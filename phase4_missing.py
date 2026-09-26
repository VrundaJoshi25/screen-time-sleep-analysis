"""Phase 4: Missing-data analysis on the REAL dataset.
Scenario: suppose some students skipped Q11 (screen use before sleep).
We know the FULL-DATA truth (slope = +0.383), so we can measure the bias
that each mechanism and each handling method introduces.
Mechanisms simulated on real data (10% missing overall):
  MCAR: missing at random, independent of everything
  MAR : missingness depends on OBSERVED stress (high-stress students skip more)
  MNAR: missingness depends on the MISSING VALUE itself (every-night users hide it)
Methods: complete-case (listwise), mean imputation, conditional-mean imputation
(by stress group; sensible under MAR).
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import statsmodels.api as sm

import os
FOLDER = os.path.dirname(os.path.abspath(__file__)) + os.sep
d = pd.read_csv(FOLDER + "analysis_data.csv")
x = d["screen_freq"].astype(float).copy()
y = d["sleep_hours"].astype(float)
stress = d["stress"].astype(int)
rng = np.random.default_rng(7)
N = len(d)

def slope(xx, yy):
    m = sm.OLS(yy, sm.add_constant(xx)).fit()
    return m.params.iloc[1], m.bse.iloc[1], m.rsquared

truth, truth_se, _ = slope(x, y)
out = ["FULL DATA truth: slope = %+.4f (SE %.4f)" % (truth, truth_se)]

def make_mask(mech):
    p = np.zeros(N)
    if mech == "MCAR":
        p[:] = 0.10
    elif mech == "MAR":   # depends on observed stress: stress 4 -> 22%, 3 -> 8%, else 3%
        p = np.where(stress == 4, 0.22, np.where(stress == 3, 0.08, 0.03))
    elif mech == "MNAR":  # depends on screen use itself: every-night users hide it
        p = np.where(x == 5, 0.30, np.where(x == 4, 0.05, 0.02))
    return rng.random(N) < p

results = {}
for mech in ["MCAR", "MAR", "MNAR"]:
    mask = make_mask(mech)
    n_miss = int(mask.sum())
    # complete case
    s_cc, se_cc, r2_cc = slope(x[~mask], y[~mask])
    # mean imputation
    x_mi = x.copy(); x_mi[mask] = x[~mask].mean()
    s_mi, se_mi, r2_mi = slope(x_mi, y)
    # conditional (stress-group) mean imputation
    x_ci = x.copy()
    for sv in sorted(stress.unique()):
        m_obs = (stress == sv) & ~mask
        x_ci[(stress == sv) & mask] = x[m_obs].mean()
    s_ci, se_ci, r2_ci = slope(x_ci, y)
    results[mech] = dict(n_miss=n_miss, cc=(s_cc, se_cc), mi=(s_mi, se_mi), ci=(s_ci, se_ci))
    out.append("\n%s (missing n=%d, %.1f%%):" % (mech, n_miss, 100 * n_miss / N))
    out.append("  complete-case      slope=%+.4f (SE %.4f)  bias=%+.4f" % (s_cc, se_cc, s_cc - truth))
    out.append("  mean imputation    slope=%+.4f (SE %.4f)  bias=%+.4f" % (s_mi, se_mi, s_mi - truth))
    out.append("  cond-mean imput.   slope=%+.4f (SE %.4f)  bias=%+.4f" % (s_ci, se_ci, s_ci - truth))
    if mech == "MAR":
        obs_miss_rate_high = mask[stress == 4].mean()
        out.append("  (check: missing rate among stress=4 students = %.2f)" % obs_miss_rate_high)
    if mech == "MNAR":
        out.append("  (check: missing rate among every-night users = %.2f; observed x-mean drops %.2f -> %.2f)"
                   % (mask[x == 5].mean(), x.mean(), x[~mask].mean()))

txt = "\n".join(out)
open(FOLDER + "phase4_results.txt", "w", encoding="utf-8").write(txt)
print(txt)

# ---- figure: bias of each method under each mechanism ----
fig, ax = plt.subplots(figsize=(10.5, 5.2))
methods = [("cc", "Complete-case", "#2E74B5"), ("mi", "Mean imputation", "#C00000"),
           ("ci", "Cond-mean imputation", "#375623")]
xs = np.arange(3)
for k, (key, lab, col) in enumerate(methods):
    ests = [results[m][key][0] for m in ["MCAR", "MAR", "MNAR"]]
    errs = [1.96 * results[m][key][1] for m in ["MCAR", "MAR", "MNAR"]]
    ax.errorbar(xs + (k - 1) * 0.25, ests, yerr=errs, fmt="o", color=col, capsize=4,
                ms=8, lw=1.8, label=lab)
ax.axhline(truth, color="black", ls="--", lw=1.8, label="Full-data truth (slope = %.3f)" % truth)
ax.set_xticks(xs, ["MCAR\n(random)", "MAR\n(depends on stress)", "MNAR\n(depends on screen use itself)"])
ax.set_ylabel("Estimated screen-time slope (hours/level)")
ax.set_title("Missing-data mechanisms vs handling methods — bias against the known truth\n"
             "(10% of screen-use answers deleted under each mechanism, n = 996)")
ax.legend(fontsize=9)
fig.tight_layout()
fig.savefig(FOLDER + "fig4_01_missing.png", dpi=140)
print("\nfigure saved")
