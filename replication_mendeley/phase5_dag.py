"""Phase 5: Causal DAG for screen use before sleep -> sleep duration.
Includes measured covariates (caffeine, activity, stress, year) and the
key UNMEASURED confounder proposed from domain knowledge: schedule
flexibility (free mornings / no fixed wake time).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

FOLDER = r"C:\Users\masum\Desktop\Vrunda\sleep project\\"

fig, ax = plt.subplots(figsize=(11, 7.5))
ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
ax.set_title("Causal DAG — screen use before sleep and sleep duration (n = 996 survey)",
             fontsize=13, fontweight="bold", pad=12)

pos = {
    "Screen use\nbefore sleep":      (2.2, 3.2),
    "Sleep\nduration":               (7.8, 3.2),
    "Schedule flexibility\n(UNMEASURED)": (5.0, 8.8),
    "Academic stress /\nworkload":   (1.3, 6.6),
    "Caffeine":                      (1.6, 0.9),
    "Physical\nactivity":            (8.6, 0.9),
    "Year of study":                 (7.6, 7.6),
}
COL = {"exposure": "#2E74B5", "outcome": "#375623", "conf": "#C00000",
       "unmeasured": "#8A8A8A", "proxy": "#7F5EA3"}
node_col = {
    "Screen use\nbefore sleep": COL["exposure"], "Sleep\nduration": COL["outcome"],
    "Schedule flexibility\n(UNMEASURED)": COL["unmeasured"],
    "Academic stress /\nworkload": COL["conf"], "Caffeine": COL["conf"],
    "Physical\nactivity": "#107C10", "Year of study": COL["proxy"],
}
for name, (px, py) in pos.items():
    dashed = "UNMEASURED" in name
    ax.add_patch(plt.Circle((px, py), 1.05, color=node_col[name],
                            linestyle="--" if dashed else "-", fill=True, alpha=0.95,
                            ec="black", lw=1.2, zorder=3))
    ax.text(px, py, name, ha="center", va="center", fontsize=8.6,
            color="white", fontweight="bold", zorder=4)

def arrow(a, b, label="", rad=0.0, lcol="black"):
    ax.annotate("", xy=pos[b], xytext=pos[a],
                arrowprops=dict(arrowstyle="-|>", lw=2, color=lcol, shrinkA=42, shrinkB=42,
                                connectionstyle=f"arc3,rad={rad}"))
    if label:
        mx, my = (pos[a][0] + pos[b][0]) / 2, (pos[a][1] + pos[b][1]) / 2
        ax.text(mx, my, label, fontsize=7.5, color=lcol, ha="center",
                bbox=dict(fc="white", ec="none", alpha=0.9, pad=1), zorder=5)

arrow("Screen use\nbefore sleep", "Sleep\nduration", "effect of interest\n(association found:\n+0.38 h/level, adj. +0.19)", 0.05, "#2E74B5")
arrow("Schedule flexibility\n(UNMEASURED)", "Screen use\nbefore sleep", "", -0.15)
arrow("Schedule flexibility\n(UNMEASURED)", "Sleep\nduration", "", -0.15)
arrow("Academic stress /\nworkload", "Screen use\nbefore sleep", "", -0.1)
arrow("Academic stress /\nworkload", "Sleep\nduration", "", 0.12)
arrow("Caffeine", "Screen use\nbefore sleep", "", 0.05)
arrow("Caffeine", "Sleep\nduration", "", -0.05)
arrow("Physical\nactivity", "Sleep\nduration", "", 0.05)
arrow("Year of study", "Schedule flexibility\n(UNMEASURED)", "", -0.05)
arrow("Year of study", "Screen use\nbefore sleep", "", 0.1)
arrow("Year of study", "Sleep\nduration", "", 0.12)

legend = [
    mpatches.Patch(color=COL["exposure"], label="Exposure (x)"),
    mpatches.Patch(color=COL["outcome"], label="Outcome (y)"),
    mpatches.Patch(color=COL["conf"], label="Measured confounders"),
    mpatches.Patch(color=COL["unmeasured"], label="UNMEASURED confounder (dashed)"),
    mpatches.Patch(color=COL["proxy"], label="Proxy for flexibility"),
]
ax.legend(handles=legend, loc="lower center", bbox_to_anchor=(0.5, -0.06), ncol=3, fontsize=8.5)
fig.tight_layout()
fig.savefig(FOLDER + "fig5_01_dag.png", dpi=140)

notes = """CAUSAL DAG - notes
==================
Back-door paths from Screen use to Sleep duration:
  1. Screen <- Schedule flexibility -> Sleep          (KEY, unmeasured)
  2. Screen <- Academic stress/workload -> Sleep      (measured: adjusted in MLR)
  3. Screen <- Caffeine -> Sleep                      (measured: adjusted)
  4. Screen <- Year -> Schedule flexibility -> Sleep  (year partially proxies flexibility)
  5. Screen <- Year -> Sleep                          (adjusted in MLR2)

Minimal adjustment set (if all measured): {Schedule flexibility, Stress} or
{Schedule flexibility, Year, Caffeine}. BUT schedule flexibility is NOT in the
survey, so full adjustment is impossible with this dataset.

Interpretation of results in causal terms:
  - Unadjusted association: +0.383 h/level.
  - After adjusting for measured confounders (caffeine, activity, stress,
    year, gender): +0.185 h/level (48% attenuated) -> paths 2,3,5 carried
    about half the raw association.
  - The remaining +0.185 CANNOT be given a causal reading: path 1
    (schedule flexibility) remains unblocked, and domain knowledge says it
    is strong (students with free mornings both binge screens nightly and
    sleep long). Reverse causation (people who sleep late use screens
    longer) is also plausible.
  - Physical activity enters only as a cause of sleep (protective),
    not a confounder of the screen-sleep path.

Conclusion: report an ASSOCIATION, not an effect. To identify the causal
effect one needs to measure schedule flexibility (first-class time,
commute, chronotype) or randomize bedtime screen use.
"""
open(FOLDER + "phase5_dag_notes.txt", "w", encoding="utf-8").write(notes)
print(notes)
print("figure saved")
