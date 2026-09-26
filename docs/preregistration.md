# Pre-registration — Main Study (Act 2)

**Date written:** 26 September 2026 — *before any data collection for the main study.*

This document fixes the study question, hypotheses, design, and analysis plan
in advance. Nothing here may be edited after data collection begins; changes,
if any, must be appended as dated amendments.

## Research question

> Does daily screen time predict sleep duration among university students?

## Hypotheses

- **H1 (expected):** more daily screen time is associated with **less** sleep (negative slope).
- **H0:** there is no meaningful association.

**Equivalence margin (decided in advance):** an effect smaller than **10 minutes
of sleep per hour of daily screen time** (|β| < 0.167 h per screen-hour) is
declared *practically negligible*. If the entire 95% CI for the slope falls
inside (−0.167, +0.167), we declare the effect equivalent to zero (TOST logic),
not merely "fail to reject".

## Design

- **Sample:** university students; anonymous Google Form; consent-first.
- **Strata (4):** gender (M/F) × year-group (Junior = 1st/2nd year; Senior = 3rd year + PG).
- **Quota:** ≥ 25 complete responses per stratum → target n ≥ 100. Collection
  does not stop until every stratum cell is full.
- **Power (verified computationally):** for r = 0.3, α = 0.05 two-sided,
  80% power requires **n = 84**; at n = 100 power = **0.87**. (Pilot had ~8%
  power at its observed |r| = 0.105 — that is why the pilot was inconclusive.)
- **Key measurement upgrade:** screen time is copied from the phone's own
  Screen Time / Digital Wellbeing weekly average — **logged, not recalled**.

## Planned analysis (fixed in advance)

1. Cleaning with a written rulebook (impossible values: sleep > 14 h or
   screen > 20 h → set missing; every drop logged).
2. SLR `sleep ~ screen_time`, then MLR `+ workload + caffeine + gender + exercise`.
3. Inference: HC3 robust SEs + bootstrap CI (10,000 resamples), 95% CIs for all coefficients.
4. Diagnostics: residual plots, Q-Q, Cook's distance, VIF.
5. Missing-data audit (MCAR/MAR/MNAR discussion of skipped questions).
6. Bonus: Q9 — sleep of pre-bed screen users vs non-users (two-group comparison).
7. Reporting: effect sizes in **minutes of sleep**, CIs as "fences", plus the
   equivalence verdict against the margin above.

## Sign-off

Written and dated before the Google Form is published.
