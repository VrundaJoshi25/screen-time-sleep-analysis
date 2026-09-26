# Screen Time & Sleep — A Multi-Dataset Statistical Study

> Does screen use before bedtime cost students sleep? A complete statistical investigation — from a 30-student pilot to a 996-student analysis — engineered as a reproducible product: SQL layer, automated tests, CI, and a pre-registered follow-up study in flight.

![tests](https://github.com/VrundaJoshi25/screen-time-sleep-analysis/actions/workflows/ci.yml/badge.svg)

## Headline findings (completed work)

| Study | n | Result |
|---|---|---|
| **Pilot** (DAU stratified survey, paired exam/regular weeks) | 30 | screen → sleep slope ≈ 0 (p = 0.58 / 0.90); exam-week sleep drops **−1.15 h** with barely any change in screen time → workload, not screens |
| **Main analysis** (Mendeley student survey, CC BY 4.0) | 996 | **positive** association: ρ = +0.23 (p ≈ 2×10⁻¹³); +0.38 h per screen-frequency level, **+0.19 h after confounder control** |

**The story the data tells:** the popular claim "bedtime scrolling costs sleep" is *not*
supported by either dataset. The only positive screen–sleep association we found halves
under adjustment for caffeine/stress/activity — consistent with an unmeasured confounder
(**schedule flexibility**: students who can sleep late do both), identified a priori in our
causal DAG.

**What the analysis includes** (all in `replication_mendeley/`, full write-up in
[`replication_mendeley/REPORT.md`](replication_mendeley/REPORT.md)):
data-quality screening · EDA with group-size-aware inference (Welch tests) · Spearman/Pearson/
ordinal-logistic triangulation · OLS with HC3 robust SEs · residual & Cook's-distance
diagnostics · confounding control (MLR) · MCAR/MAR/MNAR missing-data simulation on real data ·
causal DAG with back-door analysis · cross-study comparison.

## Engineering (why this is a product, not homework)

```
├── notebooks/                pilot analysis notebook (SLR/MLR, diagnostics, MCAR/MAR/MNAR)
├── replication_mendeley/     main analysis sub-project: REPORT.md, 9-script pipeline, figures
├── src/                      reusable code: cleaning.py (typed rulebook), NHANES pipeline
├── tests/                    pytest suite for cleaning rules — 5 tests
├── sql/                      analysis.sql + run_sql.py — every question answered twice (pandas + SQL)
├── docs/                     preregistration.md · google_form_spec.md · nhanes_dictionary.md
├── data/raw|clean/           raw data (never edited) → cleaned outputs built by code
├── .github/workflows/ci.yml  tests run on every push (badge above)
└── requirements.txt          pinned versions
```

```bash
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
python -m pytest tests/ -q                  # cleaning-rule tests
python sql/run_sql.py                       # SQL layer (GROUP BY / CTE / window functions)
cd replication_mendeley && python prepare_data.py   # full main-analysis pipeline
```

## In progress / future work

- **Pre-registered main study (n ≥ 100, data collection underway).** Quota-balanced
  (25 per stratum: gender × year-group), phone-log screen time instead of recalled guesses,
  87% power at r = 0.3. Hypotheses and analysis plan are locked in
  [`docs/preregistration.md`](docs/preregistration.md); questionnaire is copy-paste ready in
  [`docs/google_form_spec.md`](docs/google_form_spec.md). Planned outputs: SLR/MLR with
  bootstrap CIs, equivalence testing against a pre-registered ±10 min/h margin, SQL layer on
  the new data.
- **NHANES national dataset (under evaluation).** 2015–2016 cycle already downloaded and
  preliminarily analyzed (`data/raw/nhanes/`, `docs/nhanes_dictionary.md`,
  `docs/nhanes_quick_results.txt`; ~5,944 weighted adults). Integration into the comparison
  is a deliberate, pending decision — measurement differences (TV/computer hours vs student
  phone use) and the right age frame are being evaluated first. Planned: age-stratified
  analysis and design-based standard errors.
- **Longer term:** objective phone-log screen measurement at scale; live dashboard.

## Data sources

1. Lamba, Garg, Singh, Joshi — *DAU pilot survey* (IT590, Winter 2026), n = 30.
2. Abdullah, A. — *Student Insomnia & Educational Outcomes Dataset*, Mendeley Data,
   DOI [10.17632/5mvrx4v62z.2](https://doi.org/10.17632/5mvrx4v62z.2) (CC BY 4.0), n = 996.
3. CDC/NCHS — *NHANES 2015–2016* (DEMO_I, SLQ_I, PAQ_I), public use — currently exploratory.
