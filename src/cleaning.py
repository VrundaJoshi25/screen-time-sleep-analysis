"""Cleaning functions for the main-study survey (Act 2).
Rulebook (written in advance, docs/preregistration.md):
  - every value passes through a typed cleaner that returns NaN on failure
    (never crashes, never guesses)
  - impossible values are set missing, NOT deleted: sleep > 14 h, screen > 20 h,
    age outside 15-60, caffeine > 15, exercise > 7, quality outside 1-5
  - every row-level drop is justified in the cleaning log
"""
import numpy as np
import pandas as pd

LIMITS = {
    "age": (15, 60),
    "screen_hours": (0, 20),
    "screen_hours_rec": (0, 20),
    "sleep_hours": (0, 14),
    "workload_hours": (0, 16),
    "caffeine_servings": (0, 15),
    "exercise_days": (0, 7),
    "sleep_quality": (1, 5),
}


def to_numeric(value):
    """Convert a raw answer to float; return NaN for anything unparsable."""
    if value is None:
        return np.nan
    try:
        return float(str(value).strip().replace(",", "."))
    except (ValueError, TypeError):
        return np.nan


def clean_bounded(value, lo, hi):
    """Numeric value forced inside [lo, hi]; outside -> NaN (impossible value)."""
    v = to_numeric(value)
    if np.isnan(v) or v < lo or v > hi:
        return np.nan
    return v


def clean_sleep(value):
    return clean_bounded(value, *LIMITS["sleep_hours"])


def clean_screen(value):
    return clean_bounded(value, *LIMITS["screen_hours"])


def clean_age(value):
    return clean_bounded(value, *LIMITS["age"])


def clean_yes_no(value):
    """Normalize a yes/no answer to 1/0; anything else -> NaN."""
    s = str(value).strip().lower()
    if s in ("yes", "y", "1", "true"):
        return 1
    if s in ("no", "n", "0", "false"):
        return 0
    return np.nan


def make_stratum(gender, program_year):
    """2x2 stratum: gender x year-group (Junior=1st/2nd yr, Senior=3rd yr+/PG)."""
    g = str(gender).strip().lower()
    p = str(program_year).strip().lower()
    if g not in ("male", "female"):
        return np.nan
    junior = ("1st" in p) or ("2nd" in p)
    return f"{g.title()}-{'Junior' if junior else 'Senior'}"


def clean_dataset(raw):
    """Clean a raw responses DataFrame -> (clean_df, cleaning_log dict)."""
    df = raw.copy()
    log = {"rows_in": len(df), "cells_set_missing": {}, "rows_dropped": 0,
           "drop_reasons": []}
    numeric_cols = {"age": clean_age, "screen_hours": clean_screen,
                    "screen_hours_rec": clean_screen, "sleep_hours": clean_sleep,
                    "workload_hours": lambda v: clean_bounded(v, *LIMITS["workload_hours"]),
                    "caffeine_servings": lambda v: clean_bounded(v, *LIMITS["caffeine_servings"]),
                    "exercise_days": lambda v: clean_bounded(v, *LIMITS["exercise_days"]),
                    "sleep_quality": lambda v: clean_bounded(v, *LIMITS["sleep_quality"])}
    for col, fn in numeric_cols.items():
        if col in df.columns:
            before = df[col].notna().sum()
            df[col] = df[col].map(fn)
            log["cells_set_missing"][col] = int(before - df[col].notna().sum())
    if "screens_30min_bed" in df.columns:
        df["screens_30min_bed"] = df["screens_30min_bed"].map(clean_yes_no)
    if {"gender", "program_year"}.issubset(df.columns):
        df["stratum"] = [make_stratum(g, p) for g, p in
                         zip(df["gender"], df["program_year"])]
    key = ["sleep_hours", "screen_hours", "age", "gender"]
    have = [c for c in key if c in df.columns]
    bad = df[have].isna().any(axis=1)
    log["rows_dropped"] = int(bad.sum())
    log["drop_reasons"] = ["missing/invalid in %s" % c for c in have]
    log["rows_out"] = int((~bad).sum())
    return df.loc[~bad].reset_index(drop=True), log


def missing_report(df):
    """Per-column missingness audit feeding the MCAR/MAR/MNAR discussion."""
    rep = df.isna().sum()
    rep = rep[rep > 0].sort_values(ascending=False)
    return pd.DataFrame({"missing_n": rep, "missing_pct": (100 * rep / len(df)).round(1)})
