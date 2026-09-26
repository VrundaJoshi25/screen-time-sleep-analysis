"""Phase 2 - Step 2: diagnostics for OLS sleep_hours ~ screen_freq.
Residuals vs fitted, Q-Q, standardized residuals, Cook's distance,
Breusch-Pagan heteroscedasticity test, and group-level influence
(x has only 5 levels, so influence is inherently group-wise).
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import OLSInfluence
from scipy import stats

FOLDER = r"C:\Users\masum\Desktop\Vrunda\sleep project\\"
d = pd.read_csv(FOLDER + "analysis_data.csv")
x = d["screen_freq"].astype(float)
y = d["sleep_hours"].astype(float)
X = sm.add_constant(x)
m = sm.OLS(y, X).fit()

infl = OLSInfluence(m)
fitted = np.asarray(m.fittedvalues)
resid = np.asarray(m.resid)
std_r = infl.resid_studentized_internal
lev = infl.hat_matrix_diag
cooks = infl.cooks_distance[0]
n = len(d)

out = ["DIAGNOSTICS for OLS sleep_hours ~ screen_freq (n=%d)" % n]

# --- variance check ---
bp = het_breuschpagan(resid, X)
out.append("\nBreusch-Pagan heteroscedasticity test: LM=%.1f, p=%.3g %s"
           % (bp[0], bp[1], "-> variance NOT constant" if bp[1] < 0.05 else ""))
sd_by = d.assign(resid=resid).groupby(x)["resid"].agg(["std", "count"])
out.append("Residual SD by screen group:\n" + sd_by.round(3).to_string())

# --- standardized residuals ---
big = (np.abs(std_r) > 2).sum()
out.append("\n|standardized residual| > 2: %d of %d (%.1f%%; ~5%% expected under normality)"
           % (big, n, 100 * big / n))

# --- Cook's distance ---
thr = 4 / n
top = np.argsort(np.asarray(cooks))[-8:][::-1]
out.append("\nCook's D: threshold 4/n = %.4f; max = %.4f" % (thr, cooks.max()))
out.append("Top 8 observations:")
for i in top:
        out.append("  obs %-4d screen=%d sleep=%.1fh  resid=%+.2f  leverage=%.4f  CookD=%.4f"
               % (i, x.iloc[i], y.iloc[i], resid[i], lev[i], cooks[i]))
out.append("Note: leverage is IDENTICAL within each screen group (x has 5 levels),")
out.append("so influence is a GROUP property, not an individual-row property.")

# --- group-level influence: drop one screen group at a time ---
out.append("\nLeave-one-GROUP-out (refit without each screen group):")
full_slope = m.params.iloc[1]
for g in [1, 2, 3, 4, 5]:
    keep = x != g
    mg = sm.OLS(y[keep], sm.add_constant(x[keep])).fit()
    out.append("  drop group %d (n=%3d): slope %+.4f -> %+.4f  (change %+.4f, %.1f%%)"
               % (g, (~keep).sum(), full_slope, mg.params.iloc[1],
                  mg.params.iloc[1] - full_slope,
                  100 * (mg.params.iloc[1] - full_slope) / full_slope))

txt = "\n".join(out)
with open(FOLDER + "phase2_results.txt", "a", encoding="utf-8") as f:
    f.write("\n\n" + txt)
print(txt)

# ---------------- figure ----------------
fig, axes = plt.subplots(1, 3, figsize=(16, 4.8))
fig.suptitle("Regression diagnostics — OLS sleep ~ screen frequency (n = 996)", fontweight="bold")

ax = axes[0]
fj = fitted + np.random.default_rng(1).uniform(-0.05, 0.05, n)
ax.scatter(fj, resid, s=6, alpha=0.15, color="#2E74B5", edgecolors="none")
ax.axhline(0, color="#C00000", ls="--", lw=1.5)
ax.set_xlabel("Fitted values (5 levels, jittered)"); ax.set_ylabel("Residuals")
ax.set_title("Residuals vs fitted\n(stripes = the 5 x-levels; wider spread at low end)")

ax = axes[1]
(osm, osr), (sl, ic, _) = stats.probplot(std_r, dist="norm")
ax.scatter(osm, osr, s=6, alpha=0.2, color="#2E74B5", edgecolors="none")
ax.plot([-3, 3], [-3 * sl + ic, 3 * sl + ic], color="#C00000", ls="--", lw=1.5)
ax.set_xlabel("Theoretical quantiles"); ax.set_ylabel("Sample quantiles")
ax.set_title("Q-Q of standardized residuals\n(steps = discrete 5-value outcome)")

ax = axes[2]
ax.scatter(range(n), cooks, s=4, alpha=0.4, color="#2E74B5", edgecolors="none")
ax.axhline(thr, color="#C00000", ls="--", lw=1.5, label="4/n = %.4f" % thr)
i0 = top[0]
ax.annotate("max: obs %d (screen=%d, sleep=%.1fh)\n(+ 3 tied 'never-screen, <4h sleep' cases)"
            % (i0, x.iloc[i0], y.iloc[i0]), (i0, cooks[i0]),
            textcoords="offset points", xytext=(-190, -10), fontsize=7.5, color="#C00000")
ax.set_xlabel("Observation index"); ax.set_ylabel("Cook's distance")
ax.set_title("Cook's distance\n(max %.3f — no point near 1.0)" % cooks.max())
ax.legend(fontsize=8)

fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig(FOLDER + "fig2_02_diagnostics.png", dpi=140)
print("\nfigure saved")
