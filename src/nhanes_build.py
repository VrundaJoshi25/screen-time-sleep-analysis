"""NHANES 2015-2016 build + quick weighted analysis (guide Steps 26-27).
Merges DEMO_I + SLQ_I + PAQ_I, derives screen_hours and sleep_hours,
runs survey-weighted regression sleep ~ screen with robust SEs.
"""
import os
import numpy as np
import pandas as pd
import statsmodels.api as sm

import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep
RAW = ROOT + r"data\raw\nhanes\\"

demo = pd.read_sas(RAW + "DEMO_I.xpt", format="xport")[
    ["SEQN", "RIAGENDR", "RIDAGEYR", "WTMEC2YR", "SDMVPSU", "SDMVSTRA"]]
slq = pd.read_sas(RAW + "SLQ_I.xpt", format="xport")[["SEQN", "SLD012", "SLQ050"]]
paq = pd.read_sas(RAW + "PAQ_I.xpt", format="xport")[["SEQN", "PAQ710", "PAQ715", "PAD680"]]

d = demo.merge(slq, on="SEQN", how="inner").merge(paq, on="SEQN", how="inner")

# NHANES special codes: 77 = refused, 99 = don't know -> missing
for c in ["PAQ710", "PAQ715", "SLD012", "PAD680"]:
    d[c] = pd.to_numeric(d[c], errors="coerce")
    d.loc[d[c] >= 77, c] = np.nan
d["screen_hours"] = d["PAQ710"] + d["PAQ715"]
d.loc[d["screen_hours"] > 24, "screen_hours"] = np.nan
d["sleep_hours"] = d["SLD012"]
d.loc[(d["sleep_hours"] < 2) | (d["sleep_hours"] > 14), "sleep_hours"] = np.nan
d["gender"] = d["RIAGENDR"].map({1: "Male", 2: "Female"})
d["age"] = d["RIDAGEYR"]
d = d.rename(columns={"WTMEC2YR": "weight"})
work = d[["SEQN", "age", "gender", "screen_hours", "sleep_hours",
          "PAQ710", "PAQ715", "PAD680", "weight", "SDMVPSU", "SDMVSTRA"]]
work.to_csv(ROOT + r"data\clean\nhanes_work.csv", index=False)

out = ["NHANES 2015-2016 merged working file: %d rows" % len(work)]
adult = work.dropna(subset=["screen_hours", "sleep_hours", "weight"])
adult = adult[adult["age"] >= 18]
out.append("Adults 18+ with complete screen+sleep: n = %d" % len(adult))

def wreg(df, label):
    w = df["weight"] / df["weight"].mean()
    X = sm.add_constant(df["screen_hours"])
    m = sm.WLS(df["sleep_hours"], X, weights=w).fit(cov_type="HC3")
    wm = np.average(df["sleep_hours"], weights=df["weight"])
    wx = np.average(df["screen_hours"], weights=df["weight"])
    out.append("\n%s (n=%d)" % (label, len(df)))
    out.append("  weighted mean sleep = %.2f h | weighted mean screen = %.2f h/day" % (wm, wx))
    out.append("  slope = %+.4f h sleep per screen-hour (robust SE %.4f, t=%.2f, p=%.3g)"
               % (m.params.iloc[1], m.bse.iloc[1], m.tvalues.iloc[1], m.pvalues.iloc[1]))
    out.append("  95%% CI [%.4f, %.4f]  -> per +1h screen: %+.1f min sleep" %
               (m.conf_int().iloc[1, 0], m.conf_int().iloc[1, 1], 60 * m.params.iloc[1]))
    # adjusted model
    Xa = sm.add_constant(pd.DataFrame({"screen": df["screen_hours"], "age": df["age"],
                                       "male": (df["gender"] == "Male").astype(float)}))
    ma = sm.WLS(df["sleep_hours"], Xa, weights=w).fit(cov_type="HC3")
    out.append("  adjusted (+ age, gender): screen slope = %+.4f (SE %.4f, p=%.3g)"
               % (ma.params["screen"], ma.bse["screen"], ma.pvalues["screen"]))
    return m

wreg(adult, "ALL ADULTS 18+")
young = adult[(adult["age"] >= 18) & (adult["age"] <= 29)]
wreg(young, "YOUNG ADULTS 18-29 (student-age comparison group)")

txt = "\n".join(out)
open(ROOT + r"docs\nhanes_quick_results.txt", "w", encoding="utf-8").write(txt)
print(txt)

# variable dictionary
dic = """# NHANES variable dictionary (2015-2016 cycle, "I" files)

Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2015/DataFiles/ (CDC/NCHS, public use).
Cycle choice: 2015-2016 is the most recent cycle that includes the dedicated
screen-time questions; the 2017-2018 cycle DROPPED PAQ710/PAQ715 (only general
sedentary minutes PAD680 remained).

| Variable | File | Meaning | Codes |
|---|---|---|---|
| SEQN | all | respondent ID (merge key) | - |
| RIAGENDR | DEMO_I | gender | 1=Male 2=Female |
| RIDAGEYR | DEMO_I | age in years | 0-79, 80+ top-coded |
| WTMEC2YR | DEMO_I | MEC examination weight (2-yr) | used for weighted analysis |
| SDMVPSU / SDMVSTRA | DEMO_I | design PSU / strata | (noted for design-based SEs) |
| SLD012 | SLQ_I | usual sleep hours on weekdays | 2-14 valid; 77/99 = refused/DK |
| SLQ050 | SLQ_I | ever told doctor had trouble sleeping? | 1=Yes 2=No |
| PAQ710 | PAQ_I | daily hours watching TV/videos (past 30 d) | 0-24; 77/99 missing |
| PAQ715 | PAQ_I | daily hours computer/games (past 30 d) | 0-24; 77/99 missing |
| PAD680 | PAQ_I | total daily sedentary minutes | 0-1320; 7777/9999 missing |

Derived: screen_hours = PAQ710 + PAQ715 (NaN if >24);
sleep_hours = SLD012 (valid 2-14 h);
analysis population: adults 18+ with complete screen+sleep+weight.
"""
open(ROOT + r"docs\nhanes_dictionary.md", "w", encoding="utf-8").write(dic)
print("\ndictionary written")
