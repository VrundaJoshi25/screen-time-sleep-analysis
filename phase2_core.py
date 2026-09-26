"""Phase 2 - Step 1: core analysis of screen use -> sleep duration.
  - Pearson + Spearman correlations
  - OLS regression on midpoint hours (sleep_hours ~ screen_freq)
  - Ordinal logistic regression on the original 5-level sleep outcome (robustness)
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.miscmodels.ordinal_model import OrderedModel
from scipy import stats

import os
FOLDER = os.path.dirname(os.path.abspath(__file__)) + os.sep
d = pd.read_csv(FOLDER + "analysis_data.csv")
x = d["screen_freq"].astype(float)
y = d["sleep_hours"].astype(float)

out = []
# ---------------- correlations ----------------
r_p, p_p = stats.pearsonr(x, y)
rho, p_s = stats.spearmanr(x, y)
tau, p_t = stats.kendalltau(x, y)
out.append("CORRELATIONS (screen_freq vs sleep):")
out.append("  Pearson  r   = %+.4f (p = %.3g)   [on midpoint hours]" % (r_p, p_p))
out.append("  Spearman rho = %+.4f (p = %.3g)   [rank-based, primary for ordinal data]" % (rho, p_s))
out.append("  Kendall  tau = %+.4f (p = %.3g)" % (tau, p_t))

# ---------------- OLS ----------------
X = sm.add_constant(x)
m = sm.OLS(y, X).fit()
out.append("\nOLS: sleep_hours = b0 + b1 * screen_freq")
out.append("  b0 (intercept) = %.3f  (SE %.3f)" % (m.params.iloc[0], m.bse.iloc[0]))
out.append("  b1 (screen)    = %+.3f hours per screen-frequency level (SE %.3f)" % (m.params.iloc[1], m.bse.iloc[1]))
out.append("  t = %.2f, p = %.3g, 95%% CI [%.3f, %.3f]" % (m.tvalues.iloc[1], m.pvalues.iloc[1], *m.conf_int().iloc[1]))
out.append("  R^2 = %.4f  (screen use explains %.1f%% of sleep-duration variance)" % (m.rsquared, 100 * m.rsquared))
out.append("  RMSE = %.3f hours" % np.sqrt(m.mse_resid))

# ---------------- ordinal logistic (robustness) ----------------
yord = d["sleep_ord"].astype(int)
try:
    om = OrderedModel(yord, x, distr="logit")
    res = om.fit(method="bfgs", disp=False)
    b = res.params["screen_freq"]
    out.append("\nORDINAL LOGISTIC (sleep category ~ screen_freq):")
    out.append("  coef = %+.4f (SE %.4f, p = %.3g)" % (b, res.bse["screen_freq"], res.pvalues["screen_freq"]))
    out.append("  odds ratio per level = %.3f  -> each step up in screen frequency multiplies the" % np.exp(b))
    out.append("  odds of being in a LONGER sleep category by %.2f" % np.exp(b))
    ord_ok = True
except Exception as e:
    out.append("\nOrdinal logistic failed: %r" % e)
    ord_ok = False

txt = "\n".join(out)
open(FOLDER + "phase2_results.txt", "w", encoding="utf-8").write(txt)
print(txt)

# ---------------- figure: jittered scatter + OLS line ----------------
rng = np.random.default_rng(0)
xj = x + rng.uniform(-0.18, 0.18, len(x))
yj = y + rng.uniform(-0.42, 0.42, len(y))
fig, ax = plt.subplots(figsize=(9, 5.5))
ax.scatter(xj, yj, s=8, alpha=0.12, color="#2E74B5", edgecolors="none")
gm = d.groupby("screen_freq")["sleep_hours"].mean()
ax.plot(gm.index, gm.values, "o-", color="#C00000", lw=2, ms=8, label="group means", zorder=5)
xs = np.array([0.8, 5.2])
ax.plot(xs, m.params.iloc[0] + m.params.iloc[1] * xs, color="black", lw=1.8, ls="--",
        label="OLS fit: sleep = %.2f %+.2fx" % (m.params.iloc[0], m.params.iloc[1]))
ax.set_xticks([1, 2, 3, 4, 5], ["Never", "Rarely", "Sometimes", "Often", "Every\nnight"])
ax.set_xlabel("Device use before sleep (frequency)")
ax.set_ylabel("Sleep duration (midpoint hours, jittered)")
ax.set_title("Screen use before sleep vs sleep duration — positive trend (n = 996)\n"
             "Spearman ρ = %.3f (p = %.1g), OLS slope = %+.3f h/level" % (rho, p_s, m.params.iloc[1]))
ax.legend()
fig.tight_layout()
fig.savefig(FOLDER + "fig2_01_scatter_fit.png", dpi=140)
print("\nfigure saved")
