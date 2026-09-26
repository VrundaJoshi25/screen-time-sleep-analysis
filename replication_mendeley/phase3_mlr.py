"""Phase 3: Confounding control.
Does the screen->sleep association survive adjustment for caffeine,
physical activity, academic stress, year of study, gender?
MLR1: sleep ~ screen + caffeine + activity + stress
MLR2: MLR1 + year dummies + gender
Robustness: ordinal logistic on the 5-level outcome.
All OLS inference uses HC3 robust SEs (heteroscedasticity from Phase 2).
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.miscmodels.ordinal_model import OrderedModel

FOLDER = r"C:\Users\masum\Desktop\Vrunda\sleep project\\"
d = pd.read_csv(FOLDER + "analysis_data.csv")
out = []

def fit_report(formula, label, cov="HC3"):
    m = smf.ols(formula, data=d).fit(cov_type=cov)
    b = m.params["screen_freq"]; se = m.bse["screen_freq"]
    ci = m.conf_int().loc["screen_freq"]
    out.append("%s: screen coef = %+.4f (robust SE %.4f, t=%.2f, p=%.3g, CI[%.3f, %.3f]), R2=%.3f"
               % (label, b, se, m.tvalues["screen_freq"], m.pvalues["screen_freq"], ci[0], ci[1], m.rsquared))
    return m

m0 = fit_report("sleep_hours ~ screen_freq", "SLR (unadjusted)")
m1 = fit_report("sleep_hours ~ screen_freq + caffeine + activity + stress", "MLR1 (+ caffeine, activity, stress)")
m2 = fit_report("sleep_hours ~ screen_freq + caffeine + activity + stress + C(year) + C(gender)",
                "MLR2 (+ year, gender)")

out.append("\nMLR1 full table (robust SEs):")
for v in ["screen_freq", "caffeine", "activity", "stress"]:
    b, se, p = m1.params[v], m1.bse[v], m1.pvalues[v]
    out.append("  %-12s %+.4f  (SE %.4f, p=%.3g)" % (v, b, se, p))
out.append("MLR2 full table (robust SEs):")
for v in m2.params.index:
    if v in ("Intercept",): continue
    b, se, p = m2.params[v], m2.bse[v], m2.pvalues[v]
    out.append("  %-28s %+.4f  (SE %.4f, p=%.3g)" % (v, b, se, p))

# ordinal logistic robustness (multivariate)
try:
    Xo = d[["screen_freq", "caffeine", "activity", "stress"]].astype(float)
    res = OrderedModel(d["sleep_ord"].astype(int), Xo, distr="logit").fit(method="bfgs", disp=False)
    out.append("\nORDINAL LOGISTIC (multivariate):")
    for v in Xo.columns:
        b, se, p = res.params[v], res.bse[v], res.pvalues[v]
        out.append("  %-12s %+.4f (SE %.4f, p=%.3g)  OR=%.3f" % (v, b, se, p, np.exp(b)))
except Exception as e:
    out.append("ordinal logistic failed: %r" % e)

txt = "\n".join(out)
open(FOLDER + "phase3_results.txt", "w", encoding="utf-8").write(txt)
print(txt)

# ---- figure: screen coefficient across models + MLR1 coefficients ----
fig, axes = plt.subplots(1, 2, figsize=(12.5, 5))
fig.suptitle("Confounding control: does the screen-time coefficient survive adjustment?", fontweight="bold")

ax = axes[0]
labels = ["Unadjusted\n(SLR)", "+ caffeine,\nactivity, stress\n(MLR1)", "+ year, gender\n(MLR2)"]
coefs = [m0.params["screen_freq"], m1.params["screen_freq"], m2.params["screen_freq"]]
errs = [1.96 * m.bse["screen_freq"] for m in (m0, m1, m2)]
ax.bar(range(3), coefs, yerr=errs, capsize=5, color=["#2E74B5", "#4BACC6", "#1F4E79"], alpha=0.9)
for i, c in enumerate(coefs):
    ax.text(i, c + 0.02, f"{c:+.3f}", ha="center", fontweight="bold", fontsize=10)
ax.axhline(0, color="black", lw=1)
ax.set_xticks(range(3), labels, fontsize=8.5)
ax.set_ylabel("Screen-time coefficient (hours per level, 95% CI)")
ax.set_title("A. Screen coefficient before/after adjustment")

ax = axes[1]
vars_ = ["screen_freq", "caffeine", "activity", "stress"]
names = ["Screen use\n(per level)", "Caffeine\n(per level)", "Physical activity\n(per level)", "Academic stress\n(per level)"]
b = [m1.params[v] for v in vars_]
e = [1.96 * m1.bse[v] for v in vars_]
p = [m1.pvalues[v] for v in vars_]
colors = ["#C00000" if pv < 0.05 else "#999999" for pv in p]
ax.barh(range(4), b, xerr=e, capsize=5, color=colors, alpha=0.85)
ax.axvline(0, color="black", lw=1)
ax.set_yticks(range(4), names, fontsize=9)
for i, (bv, pv) in enumerate(zip(b, p)):
    ax.text(bv + (0.02 if bv >= 0 else -0.02), i, f"{bv:+.3f}" + ("*" if pv < 0.05 else " ns"),
            va="center", ha="left" if bv >= 0 else "right", fontsize=9, fontweight="bold")
ax.set_title("B. MLR1 coefficients (red = p<0.05)")
ax.set_xlabel("Effect on sleep duration (hours, 95% CI)")
fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig(FOLDER + "fig3_01_mlr.png", dpi=140)
print("\nfigure saved")
