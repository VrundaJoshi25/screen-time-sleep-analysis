# Screen Time & Sleep — The Complete Study

> Does daily screen time predict how long students sleep? A three-act research arc: a 30-student pilot, a powered main study (in data collection), and replication on US national data — plus an external validation on 996 students. Fully reproducible: `src/`, tests, CI, SQL.

![tests](https://github.com/VrundaJoshi25/screen-time-sleep-analysis/actions/workflows/ci.yml/badge.svg)

## The arc

| Act | Study | n | Status | Headline |
|---|---|---|---|---|
| 1 | **Pilot** (DAU stratified survey, paired exam/regular weeks) | 30 | ✅ done | screen slope ≈ 0, ns — but only ~8% power; exam week −1.15 h sleep (workload-driven) |
| — | **External validation** (Mendeley student survey) | 996 | ✅ done | ρ = +0.23, +0.38 h per frequency level (positive; confounder-adjusted +0.19) |
| 2 | **Main study** (pre-registered, quota 25×4, phone-log screen time) | ~100 | 🔄 collecting | designed & powered (87% at r = 0.3); form ready |
| 3 | **National replication** (NHANES 2015-16, survey-weighted) | 5,944 | ✅ done | +1.3 min sleep per screen-hour (p = .0005) — practically zero; 18–29 y: ≈ 0, ns |

**The evidence so far, in one sentence:** across three real datasets there is no
evidence that screen time costs students sleep — the powered national estimate is
a practically negligible **+1.3 minutes of sleep per hour of daily screen time**,
and the largest effects appear only where confounding (schedule flexibility) can operate.

## Repository structure

```
├── notebooks/                    Act 1 pilot notebook (SLR/MLR, diagnostics, MCAR/MAR/MNAR)
├── replication_mendeley/         External validation sub-project (996 students): REPORT.md,
│                                 full pipeline (prepare_data → phase6), figures, results
├── docs/
│   ├── preregistration.md        Act 2 hypotheses + analysis plan, fixed BEFORE data collection
│   ├── google_form_spec.md       copy-paste-ready questionnaire (12 questions, quota plan)
│   ├── nhanes_dictionary.md      NHANES variable dictionary + cycle-choice rationale
│   └── nhanes_quick_results.txt  weighted national estimates
├── data/
│   ├── raw/nhanes/               NHANES 2015-2016 XPT files (never edited)
│   └── clean/                    nhanes_work.csv (built by src/nhanes_build.py), SQLite db
├── src/                          reusable code: cleaning.py (main study), nhanes pipeline
├── tests/                        pytest suite for cleaning rules (5 tests)
├── sql/                          analysis.sql (main study), analysis_nhanes.sql, run_sql.py
├── .github/workflows/ci.yml      tests run on every push (badge above)
└── requirements.txt              pinned versions
```

## Key results (all numbers traceable to files above)

**Act 3 — NHANES 2015-16** (weighted, adults 18+, n = 5,944): sleep = **+0.022 h per
screen-hour** (robust 95% CI [+0.010, +0.034]; adjusted for age/gender +0.023). Young
adults 18–29 (n = 1,244): +0.014 h, CI [−0.013, +0.042], p = 0.31 — the whole CI sits
inside the pre-registered equivalence margin (±10 min/h): **a national equivalence result.**

**External validation** (996 students): positive association (ρ = +0.23) that halves
after adjustment (+0.383 → +0.185 h/level) — consistent with confounding by
*schedule flexibility* (see the DAG in `replication_mendeley/`).

**Act 1 pilot** (30 students, paired): slope ≈ 0 (p = 0.58/0.90); exam-week sleep
drops 1.15 h while screen time barely moves.

## Reproduce

```bash
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
python -m pytest tests/ -q            # cleaning-rule tests
python sql/run_sql.py                 # SQL layer on NHANES (GROUP BY / CTE / window)
python src/nhanes_build.py            # rebuild NHANES working data + weighted models
cd replication_mendeley && python prepare_data.py   # external-validation pipeline
```

## Data sources

1. Lamba, Garg, Singh, Joshi — *DAU pilot survey* (IT590, Winter 2026), n = 30.
2. Abdullah, A. — *Student Insomnia & Educational Outcomes Dataset*, Mendeley Data,
   DOI 10.17632/5mvrx4v62z.2 (CC BY 4.0), n = 996.
3. CDC/NCHS — *NHANES 2015-2016* (DEMO_I, SLQ_I, PAQ_I), public use,
   https://wwwn.cdc.gov/nchs/nhanes/ (cycle chosen because it retains the dedicated
   TV/computer screen-time questions PAQ710/PAQ715).
