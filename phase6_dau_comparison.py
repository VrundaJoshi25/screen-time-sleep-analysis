"""Phase 6: DAU pilot (own study, n=30, paired exam/regular) vs Mendeley
replication (n=996). Builds the comparison table and a forest-style figure.
DAU values are the real published summary statistics from the assignment
report / analysis notebook (STATS_PROJECT_REPORT.docx).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

import os
FOLDER = os.path.dirname(os.path.abspath(__file__)) + os.sep

# --- DAU pilot: real values from the report/notebook ---
dau = dict(n=30,
           exam=dict(b1=-0.001351, se=0.002422, r=-0.1048, p=0.5816, r2=0.0110,
                     mean_sleep=5.63, mean_screen=150.13),
           reg=dict(b1=-0.000532, se=0.004271, r=-0.0235, p=0.9017, r2=0.0006,
                    mean_sleep=6.78, mean_screen=133.30),
           power30=0.081, n_needed_80=711)
# 95% CI for DAU slope (t df=28)
tcrit = stats.t.ppf(0.975, 28)
dau["exam"]["lo"] = dau["exam"]["b1"] - tcrit * dau["exam"]["se"]
dau["exam"]["hi"] = dau["exam"]["b1"] + tcrit * dau["exam"]["se"]
dau["reg"]["lo"] = dau["reg"]["b1"] - tcrit * dau["reg"]["se"]
dau["reg"]["hi"] = dau["reg"]["b1"] + tcrit * dau["reg"]["se"]

# --- Mendeley: ours (from phase2/3) ---
men = dict(n=996, b1=0.3829, lo=0.279, hi=0.487, rho=0.230, p=2.03e-13,
           adj_b1=0.1846, adj_lo=0.077, adj_hi=0.292)

comp = f"""CROSS-STUDY COMPARISON - DAU pilot vs independent replication
================================================================

                        DAU pilot (own study)          Mendeley replication
----------------------  ---------------------------    ---------------------------
Sample                  n = 30, DAU (India)            n = 996, DIU (Bangladesh)
Design                  paired: exam + regular week    cross-sectional
Screen-time measure     MINUTES before sleep           FREQUENCY (nights/week)
Sleep measure           hours (self-reported)          hours in ranges (midpoints)

SLR slope (screen)      exam:    -0.0014 (p=0.58)      +0.383 h/level (p=2e-30)
                        regular: -0.0005 (p=0.90)
95% CI (exam)           [{dau['exam']['lo']:.4f}, {dau['exam']['hi']:.4f}]  [{men['lo']:.3f}, {men['hi']:.3f}]
Correlation             r = -0.105 / -0.024 (ns)       Spearman rho = +0.230 (p=2e-13)
R^2                     0.011 / 0.001                  0.125
Adjusted (MLR)          screen coef ~ 0 (ns)           +0.185 h/level (p=8e-04)
Statistical power       ~8% (needs n~711 for r=-0.105) >99% for rho=0.23 at n=996

Sleep by week type      exam 5.63h < regular 6.78h     (no week-type measured)
(-1.15h in exam week while screen time rose only +17min)

WHY THE TWO STUDIES CAN BOTH BE "RIGHT"
1. Power: the DAU pilot's CI for the exam-week slope is
   [{dau['exam']['lo']:.4f}, {dau['exam']['hi']:.4f}] h/min -> per 100 min of screen time
   that is [{100*dau['exam']['lo']:.2f}, {100*dau['exam']['hi']:.2f}] h of sleep. It covers
   zero AND small positive values: the pilot could not detect an effect
   of the size found in the replication.
2. Measurement: minutes-of-use and nights-per-week tap different aspects
   of screen behaviour (intensity vs habit).
3. Population & context: different universities, countries, schedules;
   DAU data spans exam periods (where workload dominates), DIU data
   reflects typical weeks.
4. Design: DAU paired data isolates within-student week effects
   (sleep -1.15h in exam week) which cross-sectional data cannot see.

JOINT CONCLUSION
Across two real datasets there is NO evidence that more bedtime screen
use is associated with SHORTER sleep; the larger, better-powered sample
shows a modest POSITIVE association (likely confounded by schedule
flexibility). The DAU pilot adds what the big dataset cannot: during
exam weeks sleep drops sharply (-1.15h) through workload, not screens.
"""
open(FOLDER + "phase6_comparison.txt", "w", encoding="utf-8").write(comp)
print(comp)

# --- forest-style figure ---
fig, ax = plt.subplots(figsize=(10, 4.8))
rows = [
    ("DAU pilot — exam week (n=30)", dau["exam"]["b1"] * 100, dau["exam"]["lo"] * 100, dau["exam"]["hi"] * 100, "#C00000", "s"),
    ("DAU pilot — regular week (n=30)", dau["reg"]["b1"] * 100, dau["reg"]["lo"] * 100, dau["reg"]["hi"] * 100, "#E97132", "s"),
    ("Mendeley replication (n=996)\n(units: per 100-min-equivalent NOT applicable\n— plotted as slope per frequency level x0.01)", np.nan, np.nan, np.nan, "#888", None),
    ("Mendeley — unadjusted slope/100 (h)", men["b1"] / 100 * 100, men["lo"] / 100 * 100, men["hi"] / 100 * 100, "#2E74B5", "o"),
    ("Mendeley — adjusted slope/100 (h)", men["adj_b1"] / 100 * 100, men["adj_lo"] / 100 * 100, men["adj_hi"] / 100 * 100, "#1F4E79", "o"),
]
ylabels, kept = [], []
for lab, est, lo, hi, col, mk in rows:
    if np.isnan(est): continue
    kept.append((lab, est, lo, hi, col, mk))
for i, (lab, est, lo, hi, col, mk) in enumerate(kept):
    ax.plot([lo, hi], [i, i], color=col, lw=2.5)
    ax.plot(est, i, mk, color=col, ms=10)
    ylabels.append(lab)
ax.axvline(0, color="black", ls="--", lw=1.2)
ax.set_yticks(range(len(kept)), ylabels, fontsize=9)
ax.set_xlabel("Slope estimate with 95% CI  (DAU: hours of sleep per 100 min screen time;\nMendeley: rescaled slope per frequency level, /100 for display)")
ax.set_title("The two real studies side by side: pilot CIs are wide and cover zero;\nthe powered replication is precise — and positive", fontsize=11, fontweight="bold")
fig.tight_layout()
fig.savefig(FOLDER + "fig6_01_comparison.png", dpi=140)
print("\nfigure saved")
