"""Phase 1 - Step 1: distributions of all 15 survey questions (n=996)."""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import os
FOLDER = os.path.dirname(os.path.abspath(__file__)) + os.sep
df = pd.read_csv(FOLDER + "analysis_data.csv")

PLOTS = [  # (raw category column, title, ordered levels)
    ("year", "Q1 Year of study", ["First year", "Second year", "Third year", "Graduate student"]),
    ("gender", "Q2 Gender", ["Male", "Female"]),
    ("insomnia_freq", "Q3 Difficulty falling asleep", ["Never", "Rarely (1-2 times a week)", "Sometimes (3-4 times a week)", "Often (5-6 times a week)", "Every night"]),
    ("sleep_cat", "Q4 Sleep duration (hours)", ["Less than 4 hours", "4-5 hours", "6-7 hours", "7-8 hours", "More than 8 hours"]),
    ("awakenings_freq", "Q5 Night awakenings", ["Never", "Rarely (1-2 times a week)", "Sometimes (3-4 times a week)", "Often (5-6 times a week)", "Every night"]),
    ("sleep_quality_cat", "Q6 Sleep quality", ["Very poor", "Poor", "Average", "Good", "Very good"]),
    ("concentration_freq", "Q7 Poor concentration", ["Never", "Rarely", "Sometimes", "Often", "Always"]),
    ("fatigue_freq", "Q8 Daytime fatigue", ["Never", "Rarely", "Sometimes", "Often", "Always"]),
    ("skip_classes_freq", "Q9 Skip classes (sleep)", ["Never", "Rarely (1-2 times a month)", "Sometimes (1-2 times a week)", "Often (3-4 times a week)", "Always"]),
    ("deadline_impact_cat", "Q10 Impact on deadlines", ["No impact", "Minor impact", "Moderate impact", "Major impact", "Severe impact"]),
    ("screen_freq_cat", "Q11 Devices before sleep [x]", ["Never", "Rarely (1-2 times a week)", "Sometimes (3-4 times a week)", "Often (5-6 times a week)", "Every night"]),
    ("caffeine_freq_cat", "Q12 Caffeine", ["Never", "Rarely (1-2 times a week)", "Sometimes (3-4 times a week)", "Often (5-6 times a week)", "Every day"]),
    ("activity_freq_cat", "Q13 Physical activity", ["Never", "Rarely (1-2 times a week)", "Sometimes (3-4 times a week)", "Often (5-6 times a week)", "Every day"]),
    ("stress_cat", "Q14 Academic stress", ["No stress", "Low stress", "High stress", "Extremely high stress"]),
    ("performance_cat", "Q15 Academic performance", ["Poor", "Below Average", "Average", "Good", "Excellent"]),
]

fig, axes = plt.subplots(4, 4, figsize=(17, 13))
fig.suptitle("How the 996 students answered — distributions of all 15 questions",
             fontsize=15, fontweight="bold", y=0.995)
for ax, (col, title, order) in zip(axes.ravel(), PLOTS):
    pct = df[col].value_counts(normalize=True).reindex(order) * 100
    labels = [o.replace(" (", "\n(") for o in order]
    colors = ["#C00000" if col in ("screen_freq_cat", "sleep_cat") else "#2E74B5"] * len(order)
    ax.barh(range(len(order)), pct.values, color=colors, alpha=0.85)
    ax.set_yticks(range(len(order)), labels, fontsize=7.5)
    ax.invert_yaxis()
    ax.set_title(title, fontsize=10, fontweight="bold",
                 color="#C00000" if col in ("screen_freq_cat", "sleep_cat") else "black")
    for i, v in enumerate(pct.values):
        ax.text(v + 0.7, i, f"{v:.0f}%", va="center", fontsize=7.5, color="#444")
    ax.set_xlim(0, max(pct.values) * 1.22)
    ax.tick_params(axis="x", labelsize=7)
axes.ravel()[-1].axis("off")
fig.tight_layout(rect=[0, 0, 1, 0.98])
fig.savefig(FOLDER + "fig1_01_distributions.png", dpi=140)
print("figure saved")
