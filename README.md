# Screen Time & Sleep Duration: Statistical Analysis of Survey Data

> Does screen time predict how long students sleep? A stratified survey study with regression modeling, full assumption diagnostics, and an honestly reported null result.

## Overview

Academic project, M.Sc. Data Science, Dhirubhai Ambani University (Winter 2026).

- Designed and conducted a stratified survey (n = 30, 4 strata)
- Built simple and multiple linear regression (SLR / MLR) models in Python to test whether screen time predicts sleep duration, controlling for workload and caffeine intake
- Validated model assumptions with residual analysis, Q-Q plots, and Cook's Distance diagnostics
- Ran a missing-data sensitivity analysis covering the MCAR / MAR / MNAR mechanisms

## Key Result

Screen time showed **no meaningful linear relationship** with sleep duration in this sample (R-squared < 1.1%, p = 0.58).

The value of this project is the rigor, not the effect size: the null result is reported with complete diagnostics and sensitivity analysis, so every step from raw responses to conclusion is reproducible.

## Repository Structure

| Path | Contents |
|---|---|
| `notebooks/` | Analysis notebook(s): data cleaning, SLR/MLR fitting, diagnostics, sensitivity analysis |
| `data/` | Anonymized survey responses (see `data/README.md` before committing anything) |
| `requirements.txt` | Python dependencies |

## How to Run

```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook notebooks/
```

## Tools

Python, pandas, statsmodels, NumPy, Matplotlib, SciPy
