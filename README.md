# Screen Time & Sleep Duration: From a 30-Student Pilot to a 996-Student Replication

> Does screen time before bed predict how long students sleep? A stratified pilot survey at DAU (n = 30) — and a full replication on 996 real students (Mendeley Data) — with regression modeling, complete diagnostics, missing-data sensitivity, and causal-DAG reasoning.

## The arc of this project

**Part 1 — DAU pilot (Winter 2026).** Stratified survey of n = 30 DAU students (4 strata), paired exam-week / regular-week responses. Result: screen time showed **no meaningful linear relationship** with sleep duration (R² < 1.1%, p = 0.58) — but the pilot was severely underpowered (~8% power; its own analysis called for n ≈ 711). A unique pilot finding: students sleep **1.15 h less in exam weeks**, with almost no change in screen time → workload, not screens, drives exam-period sleep loss.

**Part 2 — Independent replication (this project).** Analysis of 996 real students ([Student Insomnia & Educational Outcomes Dataset](https://doi.org/10.17632/5mvrx4v62z.2), CC BY 4.0). Result: a **positive** association — more frequent bedtime screen use ↔ *longer* sleep (Spearman ρ = +0.23, p ≈ 2×10⁻¹³; OLS +0.38 h per frequency level, robust SEs; adjusted +0.19 h after caffeine/activity/stress/year/gender). The apparent paradox resolves through a causal DAG: an unmeasured confounder — **schedule flexibility** — plausibly drives both habits.

**Full write-up: [REPORT.md](REPORT.md)** — data quality screening, EDA, correlations, regression, diagnostics (residuals / Cook's distance / group influence), confounding control, MCAR–MAR–MNAR missing-data simulation on real data, causal DAG, and the cross-study comparison.

## Key results at a glance

| | DAU pilot (n = 30) | Replication (n = 996) |
|---|---|---|
| Screen → sleep slope | −0.0014 (p = 0.58) | +0.383 h/level (p = 2×10⁻³⁰) |
| 95% CI | [−0.63, +0.36] h / 100 min | [+0.28, +0.49] h/level |
| Adjusted | ≈ 0 (ns) | +0.185 h/level (p = 8×10⁻⁴) |
| Power | ~8% | >99% |
| Exam-week effect | sleep −1.15 h (workload-driven) | — |

Neither study supports the claim that bedtime screen use shortens sleep; the powered replication finds a modest positive association, best explained by schedule flexibility rather than a causal screen effect.

## Repository structure

| Path | Contents |
|---|---|
| `REPORT.md` | Full replication report (all phases, figures, discussion) |
| `notebooks/` | DAU pilot analysis notebook (SLR/MLR, diagnostics, MCAR/MAR/MNAR) |
| `data/` | Pilot data (anonymized before committing — see `data/README.md`) |
| `student_insomnia_raw.csv` | Replication raw data (996 × 16, Mendeley, CC BY 4.0) |
| `analysis_data.csv`, `codebook.txt` | Coded replication dataset |
| `prepare_data.py`, `phase1_*.py` … `phase6_*.py` | Replication pipeline, run in order |
| `fig*.png` | All figures |
| `phase*_results.txt` | Numeric outputs of each phase |

## How to run

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
python prepare_data.py         # builds analysis_data.csv
python phase1_eda.py           # then phase1_eda2, phase2_core, ... in order
```

## Tools & data citation

Python, pandas, NumPy, statsmodels, SciPy, Matplotlib.

Abdullah, A. *Student Insomnia and Educational Outcomes Dataset.* Mendeley Data, V2 (2024). DOI: [10.17632/5mvrx4v62z.2](https://doi.org/10.17632/5mvrx4v62z.2) — CC BY 4.0.
