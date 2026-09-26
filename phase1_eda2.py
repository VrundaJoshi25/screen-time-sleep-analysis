"""Phase 1 - Step 2: screen use x sleep relationship + breakdowns by year/gender."""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

import os
FOLDER = os.path.dirname(os.path.abspath(__file__)) + os.sep
d = pd.read_csv(FOLDER + "analysis_data.csv")

S_ORDER = [1, 2, 3, 4, 5]
S_LAB = ["Never", "Rarely", "Sometimes", "Often", "Every night"]
H_ORDER = [3.0, 4.5, 6.5, 7.5, 8.5]
H_LAB = ["<4h", "4-5h", "6-7h", "7-8h", ">8h"]
Y_ORDER = ["First year", "Second year", "Third year", "Graduate student"]

fig, axes = plt.subplots(2, 2, figsize=(13, 10))
fig.suptitle("Screen use before sleep vs sleep duration — first look (n = 996)",
             fontsize=14, fontweight="bold")

# --- Panel A: heatmap, % within each screen group ---
ct = pd.crosstab(d["screen_freq"], d["sleep_hours"], normalize="index") * 100
ct = ct.reindex(index=S_ORDER, columns=H_ORDER) * 1.0
ax = axes[0, 0]
im = ax.imshow(ct.values, cmap="Blues", aspect="auto", vmin=0, vmax=ct.values.max())
ax.set_xticks(range(5), H_LAB); ax.set_yticks(range(5), S_LAB)
ax.set_xlabel("Sleep duration"); ax.set_ylabel("Devices before sleep")
ax.set_title("A. Sleep-duration profile within each screen group (row %)")
for i in range(5):
    for j in range(5):
        ax.text(j, i, f"{ct.values[i, j]:.0f}%", ha="center", va="center",
                color="white" if ct.values[i, j] > ct.values.max() * 0.6 else "black", fontsize=9)
fig.colorbar(im, ax=ax, shrink=0.85, label="% of group")

# --- Panel B: mean sleep hours by screen group (95% CI) ---
ax = axes[0, 1]
means, los, his = [], [], []
for s in S_ORDER:
    v = d.loc[d["screen_freq"] == s, "sleep_hours"]
    m = v.mean(); ci = 1.96 * v.std(ddof=1) / np.sqrt(len(v))
    means.append(m); los.append(m - ci); his.append(m + ci)
ax.bar(range(5), means, color="#2E74B5", alpha=0.85, yerr=[np.array(means) - np.array(los), np.array(his) - np.array(means)], capsize=4)
for i, m in enumerate(means):
    ax.text(i, m + 0.12, f"{m:.2f}", ha="center", fontsize=9, fontweight="bold")
ax.set_xticks(range(5), S_LAB, fontsize=8)
ax.set_ylabel("Mean sleep (midpoint hours)"); ax.set_ylim(0, 9)
ax.set_title("B. Mean sleep duration by screen-use group (95% CI)")

# --- Panel C: mean sleep by year and gender ---
ax = axes[1, 0]
def grp_mean_ci(df_, col, order):
    out = []
    for g in order:
        v = df_.loc[df_[col] == g, "sleep_hours"]
        out.append((v.mean(), 1.96 * v.std(ddof=1) / np.sqrt(len(v)), len(v)))
    return out
yres = grp_mean_ci(d, "year", Y_ORDER)
gres = grp_mean_ci(d, "gender", ["Male", "Female"])
xpos = np.arange(len(Y_ORDER))
ax.bar(xpos - 0.0, [r[0] for r in yres], width=0.55, color="#2E74B5", alpha=0.85,
       yerr=[r[1] for r in yres], capsize=4, label="by year")
ax.bar(np.arange(2) + len(Y_ORDER) + 0.5, [r[0] for r in gres], width=0.55,
       color="#7F5EA3", alpha=0.85, yerr=[r[1] for r in gres], capsize=4, label="by gender")
ax.set_xticks(list(xpos) + list(np.arange(2) + len(Y_ORDER) + 0.5),
              ["1st yr", "2nd yr", "3rd yr", "Grad", "Male", "Female"], fontsize=8)
for i, r in enumerate(yres):
    ax.text(i - 0.0, r[0] + 0.15, f"{r[0]:.2f}\n(n={r[2]})", ha="center", fontsize=7.5)
for i, r in enumerate(gres):
    ax.text(len(Y_ORDER) + 0.5 + i, r[0] + 0.15, f"{r[0]:.2f}\n(n={r[2]})", ha="center", fontsize=7.5)
ax.set_ylabel("Mean sleep (midpoint hours)"); ax.set_ylim(0, 9.3)
ax.set_title("C. Mean sleep duration by year group and gender (95% CI)")

# --- Panel D: screen-use distribution by year (stacked %) ---
ax = axes[1, 1]
bottoms = np.zeros(len(Y_ORDER))
colors = ["#DEEAF1", "#9DC3E6", "#2E74B5", "#1F4E79", "#C00000"]
for k, s in enumerate(S_ORDER):
    vals = [(d.loc[d["year"] == y, "screen_freq"] == s).mean() * 100 for y in Y_ORDER]
    ax.bar(range(len(Y_ORDER)), vals, bottom=bottoms, color=colors[k], label=S_LAB[k], width=0.6)
    bottoms += np.array(vals)
ax.set_xticks(range(len(Y_ORDER)), ["1st yr", "2nd yr", "3rd yr", "Grad"], fontsize=8)
ax.set_ylabel("% within year group"); ax.set_ylim(0, 100)
ax.set_title("D. Screen-use-before-sleep profile by year group")
ax.legend(fontsize=7, loc="lower left")

fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(FOLDER + "fig1_02_relationship.png", dpi=140)

# ---- numeric summary ----
out = []
out.append("Mean sleep_hours by screen group (95% CI):")
for s, m, lo, hi in zip(S_ORDER, means, los, his):
    out.append("  %-12s n=%3d  mean=%.2f  CI[%.2f, %.2f]" % (S_LAB[s - 1], (d["screen_freq"] == s).sum(), m, lo, hi))
out.append("")
out.append("Mean sleep by year: " + "; ".join(f"{y}={r[0]:.2f} (n={r[2]})" for y, r in zip(Y_ORDER, yres)))
out.append("Mean sleep by gender: " + "; ".join(f"{g}={r[0]:.2f} (n={r[2]})" for g, r in zip(["Male", "Female"], gres)))
rho, p = stats.spearmanr(d["screen_freq"], d["sleep_hours"])
out.append("\nSpearman rho(screen, sleep) = %.3f (p=%.3g)" % (rho, p))
txt = "\n".join(out)
open(FOLDER + "phase1_step2_results.txt", "w", encoding="utf-8").write(txt)
print(txt)
