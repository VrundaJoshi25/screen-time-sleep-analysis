"""Tests for src/cleaning.py — run with: python -m pytest tests/ -q"""
import sys, os
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import cleaning  # noqa: E402


def test_clean_sleep_accepts_valid():
    assert cleaning.clean_sleep("7.5") == 7.5
    assert cleaning.clean_sleep(8) == 8.0
    assert cleaning.clean_sleep(" 6 ") == 6.0


def test_clean_sleep_rejects_impossible_and_garbage():
    assert np.isnan(cleaning.clean_sleep("15"))     # > 14 h: impossible
    assert np.isnan(cleaning.clean_sleep("abc"))    # garbage: fail safely
    assert np.isnan(cleaning.clean_sleep(None))
    assert np.isnan(cleaning.clean_sleep("-2"))


def test_clean_screen_bounds():
    assert cleaning.clean_screen("6.5") == 6.5
    assert np.isnan(cleaning.clean_screen("25"))    # > 20 h/day impossible
    assert np.isnan(cleaning.clean_screen("ten"))


def test_clean_yes_no():
    assert cleaning.clean_yes_no("Yes") == 1
    assert cleaning.clean_yes_no(" no ") == 0
    assert np.isnan(cleaning.clean_yes_no("maybe"))


def test_stratum_and_dataset_log():
    assert cleaning.make_stratum("Male", "B.Tech 1st year") == "Male-Junior"
    assert cleaning.make_stratum("Female", "M.Sc") == "Female-Senior"
    raw = pd.DataFrame({
        "age": ["20", "19", "abc"], "screen_hours": ["5", "6", "4"],
        "sleep_hours": ["7", "8", "7"], "gender": ["Male", "Female", "Male"],
        "program_year": ["B.Tech 1st year", "M.Sc", "B.Tech 3rd year"]})
    clean, log = cleaning.clean_dataset(raw)
    assert log["rows_in"] == 3 and log["rows_dropped"] == 1 and len(clean) == 2
    assert list(clean["stratum"]) == ["Male-Junior", "Female-Senior"]
