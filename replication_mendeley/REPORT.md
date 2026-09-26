# Screen Time Before Sleep and Sleep Duration in University Students

**A statistical analysis of 996 real survey responses, with a cross-study comparison to a 30-student paired pilot study**

---

## 1. Research question

> Does screen use before bedtime relate to how long university students sleep?

The popular hypothesis — "scrolling before bed costs you sleep" — predicts a **negative** association. This project tests it on real data, controls for the plausible confounders (caffeine, physical activity, academic stress), quantifies the influence of missing-data handling, and confronts the causal interpretation honestly with a DAG. A small paired pilot study from Dhirubhai Ambani University (DAU) is used as an independent point of comparison.

**Variables**

| Role | Variable | Measurement in the main dataset |
|---|---|---|
| Exposure (x) | Screen use before sleep | frequency: Never → Every night (5 levels) |
| Outcome (y) | Sleep duration | hours, in 5 ranges (<4 … >8), midpoints for regression |
| Covariates | Caffeine, physical activity, academic stress, year of study, gender | ordinal / categorical |

---

## 2. The data

### 2.1 Source

**Main dataset:** *Student Insomnia and Educational Outcomes Dataset* (Mendeley Data, DOI [10.17632/5mvrx4v62z.2](https://doi.org/10.17632/5mvrx4v62z.2), license CC BY 4.0). Real Google-Forms survey of **996 students** at Daffodil International University (Bangladesh), Oct–Nov 2024. 15 questions; no missing values; file `student_insomnia_raw.csv`, coded version `analysis_data.csv` with `codebook.txt`.

**Why a published dataset?** Real data can surprise; simulated data only reflects its author's assumptions. Public "student screen time & sleep" datasets were screened, and most were found to be synthetic (AI-generated) and rejected. This one is a genuine, citable survey.

**Comparison dataset:** summary statistics from our own 30-student paired DAU pilot (March 2026), published in the team's assignment report.

### 2.2 Data quality screening (and an honest self-correction)

Before analysis we stress-tested the dataset's internal logic: *88%* of students report frequent difficulty falling asleep, yet *90%* report sleeping 6+ hours. That looks contradictory only under the assumption that wake-up time is fixed. **For students it isn't**: delayed sleep onset can be fully compensated by waking later (a student who falls asleep at 6 AM can still sleep 7–8 hours). Both "incoherent" directions dissolve under flexible schedules, so the dataset was retained, with its skews documented as a sampling note: an insomnia-themed survey naturally attracts sleep-struggling respondents (**self-selection**), which matters for generalization but not for the internal association we estimate.

### 2.3 The 15 variables

All answers are self-reported and retrospective ("your typical day"). Two questions anchor the project:

- **Q11 — Devices before sleep (x):** "How often do you use electronic devices (phone, computer) before going to sleep?" — Never < Rarely (1–2/wk) < Sometimes (3–4/wk) < Often (5–6/wk) < Every night
- **Q4 — Sleep duration (y):** "<4h / 4–5h / 6–7h / 7–8h / >8h" → analyzed as the ordinal category and as midpoints (3.0, 4.5, 6.5, 7.5, 8.5 h)

Covariates: caffeine frequency (Q12), physical activity frequency (Q13), academic-workload stress (Q14), year of study (Q1), gender (Q2). Secondary sleep outcomes (Q3, Q5, Q6) and academic consequences (Q7–Q10, Q15) support robustness checks.

**Measurement note for the cross-study comparison:** this dataset measures screen exposure as *frequency* (nights/week); the DAU pilot measured *minutes*. Same construct, different ruler.

---

## 3. Exploratory analysis (Phase 1)

**Who the respondents are** (`fig1_01_distributions.png`): 48% graduate students, 42% third years, 7% second years, 2% first years; 69% male. 83% use screens before sleep often/every night; 90% sleep 6+ hours; 92% report high/extremely high academic stress; 84% use caffeine often/daily; 83% exercise often/daily. Sleep *quality* is polarized (46% poor/very poor vs 46% good/very good).

**Key relationship** (`fig1_02_relationship.png`):

- Sleep duration rises **monotonically** across screen-use groups: 6.03 → 6.73 → 7.33 → 7.76 → 7.94 h (Never → Every night); 97% of every-night users sleep 7+ hours.
- Mean sleep also rises with academic seniority (1st yr 7.16 → grad 7.88 h) and differs by gender (male 7.80 vs female 7.48 h; Welch p ≈ 5×10⁻⁵).
- Screen use before sleep *also* rises with seniority — a textbook confounding pattern (see §7).

**Sample-size discipline.** Group means from unequal group sizes were compared with Welch tests (unequal variances/sizes), never raw eyeballing. A crucial consequence: the **largest** raw gap (first vs graduate year, −0.72 h) is *not* significant (p = 0.076; n = 22, CI ±0.75 h), while a **smaller** gap (third vs graduate year, −0.28 h) is highly significant (p < 10⁻⁴) — significance depends on the difference *and* the amount of data behind each number. **All first-/second-year findings are therefore labeled exploratory** — a genuine limitation of this dataset's recruitment.

## 4. Core analysis (Phase 2)

### 4.1 Correlations and regression (`fig2_01_scatter_fit.png`)

| Method | Estimate | p-value |
|---|---|---|
| Spearman ρ (primary, ordinal) | **+0.230** | 2×10⁻¹³ |
| Pearson r (midpoints) | +0.354 | 1×10⁻³⁰ |
| Kendall τ | +0.212 | 2×10⁻¹³ |

**OLS on midpoints:** `sleep = 6.14 + 0.383 × screen-frequency`
slope **+0.383 h per level** (robust HC3 SE 0.053, t = 7.2, p ≈ 6×10⁻¹³, 95% CI [0.28, 0.49]); R² = 0.125, RMSE = 0.88 h. Each step up the screen scale ≈ +23 min of sleep; "Every night" vs "Never" ≈ +1.5 h.

**Ordinal robustness** (proportional-odds logistic on the raw 5-level outcome): odds ratio **1.96 per screen level** (p ≈ 10⁻¹⁷). The finding is not an artifact of midpoint coding.

> **Result:** the association is real, precisely estimated, and **positive** — the opposite of the folk hypothesis.

### 4.2 Diagnostics (`fig2_02_diagnostics.png`)

- **Residuals vs fitted:** five stripes (one per x-level — structural for ordinal x), centered on zero → linearity adequate at group level. Spread shrinks markedly left→right (SD 2.2 h in the n = 17 "Never" group → 0.6 h in "Every night"): **heteroscedasticity**, Breusch–Pagan p ≈ 2×10⁻²². Handled with HC3 robust standard errors (conclusion unchanged).
- **Standardized residuals:** 4.3% exceed |2| ≈ the ~5% expected; Q-Q shows the staircase of a discrete outcome; n = 996 gives CLT protection. **No outlier problem.**
- **Cook's distance:** max D = 0.113 ≪ 1.0 → **no influential individual** (with n = 996 each row is 0.1% of the data; leverage is identical within each screen group, so influence is a group property).
- **Group influence:** dropping "Every night" *strengthens* the slope (+0.38 → +0.52); dropping "Never" weakens it (−12%). The association is structurally stable.

## 5. Confounding control (Phase 3, `fig3_01_mlr.png`)

Multiple regression with robust SEs:

| Model | Screen coefficient | p-value | R² |
|---|---|---|---|
| Unadjusted | +0.383 | 6×10⁻¹³ | 0.125 |
| + caffeine, activity, stress | +0.198 | 4×10⁻⁴ | 0.179 |
| + year, gender | **+0.185** | 8×10⁻⁴ | 0.194 |

The screen coefficient **attenuates 48% but survives** measured-confounder adjustment. Multivariate ordinal logistic agrees (screen OR = 1.32, p = 0.004).

Notable secondary findings: **caffeine is positively associated with sleep duration** (+0.24 h/level, p ≈ 2×10⁻⁶; pharmacologically surprising → itself confounded); academic stress is **not** associated with sleep *duration* (p = 0.49 — consistent with stress delaying *onset*, not shortening total sleep under flexible schedules); males sleep +0.19 h more (p = 0.005).

## 6. Missing-data analysis (Phase 4, `fig4_01_missing.png`)

**Scenario:** suppose 10% of students had skipped Q11 (screen use). Because we know the full-data truth (slope +0.383), we can measure the bias each mechanism and remedy actually causes.

**Why students might not report screen time:** accidental skip (MCAR); high-stress students rushing the form (MAR — missingness predictable from observed stress); every-night users hiding heavy use out of embarrassment (MNAR — missingness depends on the missing value itself).

**Simulation on the real data** (seeded, 10% deleted under each mechanism; methods: complete-case, mean imputation, conditional-mean imputation by stress group):

| Mechanism | Complete-case | Mean imputation | Cond-mean imputation |
|---|---|---|---|
| MCAR | +0.391 (bias +0.008) | +0.391 (same slope, R² diluted 0.125→0.110) | +0.398 |
| MAR (on stress) | +0.384 (bias +0.001) | +0.384 | +0.382 (best) |
| MNAR (on screen use) | +0.394 (bias +0.011) | +0.394 | +0.401 |

**Findings:**

1. Under **MCAR**, complete-case is unbiased; mean imputation returns the *identical* slope (exact algebraic property of imputing x at x̄) but dilutes R² and treats fabricated values as real data → inference is not trustworthy.
2. Under **MAR**, conditioning imputation on the observed driver (stress) is best, as theory predicts.
3. Under our **MNAR**, the slope bias stayed small — an important subtlety: **missingness that depends on the predictor x alone does not bias the regression slope** (selection on x is ignorable for the conditional model). MNAR still corrupts prevalence estimates (the observed mean screen use drops from 4.08 to 3.99) and any method will misrepresent the hidden heavy users — which is where MNAR truly bites.

## 7. Causal reasoning (Phase 5, `fig5_01_dag.png`)

The DAG encodes the domain structure, including the **key unmeasured confounder: schedule flexibility** (free mornings / no fixed wake time) — proposed from student experience and consistent with the seniority gradients found in the data.

**Back-door paths:** (1) Screen ← Schedule flexibility → Sleep — *unmeasured*; (2) Screen ← Stress → Sleep; (3) Screen ← Caffeine → Sleep; (4) Screen ← Year → Flexibility → Sleep; (5) Screen ← Year → Sleep.

**Causal reading of the numbers:** adjustment blocked paths 2, 3, 5 (48% attenuation) — but **path 1 remains unblocked** because schedule flexibility is not in the questionnaire. The residual +0.185 h/level therefore **cannot** be read as an effect of screens on sleep; it is equally consistent with flexibility (or reverse causation: late sleepers use screens longer). Physical activity enters as a cause of sleep only. **Conclusion: report an association, not an effect.** Identifying the effect requires measuring flexibility (first-class time, commute, chronotype) or randomizing bedtime screen use.

## 8. Cross-study comparison: DAU pilot vs this dataset (Phase 6, `fig6_01_comparison.png`)

| | DAU pilot (own study) | Mendeley replication |
|---|---|---|
| Sample | n = 30, DAU (India) | n = 996, DIU (Bangladesh) |
| Design | paired exam + regular week | cross-sectional |
| Screen measure | **minutes** before sleep | **frequency** (nights/week) |
| Slope | −0.0014 (p = 0.58), −0.0005 (p = 0.90) | +0.383 (p = 2×10⁻³⁰) |
| 95% CI | exam: [−0.63, +0.36] h per 100 min | [+0.28, +0.49] h/level |
| Power | ~8% (needs n ≈ 711) | >99% |
| Exam effect | sleep **−1.15 h** in exam week (screen +17 min only) | — |

**Why both can be "right":** the pilot's CI contains zero *and* small positive effects — it could never have detected the replication's modest positive association (its own power analysis demanded n ≈ 711; the replication has 996). They also differ in measurement (minutes vs frequency), population, and design. The pilot contributes what the big dataset cannot: **during exam weeks sleep collapses (−1.15 h) while screen time barely moves — workload, not screens, drives exam-period sleep loss.**

**Joint conclusion:** across two real datasets there is **no evidence** that bedtime screen use is associated with *shorter* sleep; the better-powered sample finds a modest *positive* association, best explained by schedule flexibility.

## 9. Limitations

1. **Self-reported, retrospective** answers; screen exposure as frequency, sleep in ranges (midpoints approximate).
2. **Self-selected sample** (insomnia-themed survey → distressed respondents); 90% are 3rd-year+graduate → junior-year analyses exploratory only.
3. **Unmeasured confounding** — schedule flexibility is absent from the survey; no causal claim is made.
4. **Ordinal predictors** — OLS on coded levels assumes equal spacing; mitigated by Spearman and ordinal-logistic agreement.
5. Cross-sectional: cannot separate within-person change (the DAU paired design partially fills this).

## 10. Conclusions

1. In 996 real students, more frequent bedtime screen use is associated with **longer, not shorter, sleep** (ρ = +0.23; +0.38 h per level; robust and stable under diagnostics and missing-data scenarios).
2. Half of the association is carried by measured confounders; the remainder is plausibly explained by an **unmeasured confounder — schedule flexibility** — identified a priori and supported by seniority patterns in the data.
3. Neither this dataset nor the DAU pilot supports the folk claim that pre-sleep scrolling shortens sleep; the pilot shows exam-week sleep loss is driven by **workload**, not screens.
4. Methodological takeaways: real ordinal survey data demands rank methods and robust SEs; significance depends on effect size *and* group n (Welch discipline); selection-on-x missingness does not bias slopes; and a DAG should decide what regression can claim.

## 11. Reproducibility

Run order (Python, packages: pandas, numpy, matplotlib, scipy, statsmodels):

```
prepare_data.py          # raw CSV -> analysis_data.csv + codebook + first results
phase1_eda.py            # distributions figure
phase1_eda2.py           # relationship + year/gender breakdowns
phase2_core.py           # correlations, OLS, ordinal logistic, scatter figure
phase2_diagnostics.py    # residuals, Cook's D, robust SE, group influence
phase3_mlr.py            # confounding control (MLR1/MLR2) + figure
phase4_missing.py        # MCAR/MAR/MNAR simulation + methods figure
phase5_dag.py            # causal DAG figure + notes
phase6_dau_comparison.py # cross-study comparison + figure
```

## 12. References

1. Abdullah, A. *Student Insomnia and Educational Outcomes Dataset.* Mendeley Data, V2 (2024). DOI: 10.17632/5mvrx4v62z.2 (CC BY 4.0).
2. Lamba, S., Garg, S., Singh, A., Joshi, V. *Screen Time and Sleep Duration — DAU pilot study* (IT590 project report, 2026). Summary statistics used for cross-study comparison.
