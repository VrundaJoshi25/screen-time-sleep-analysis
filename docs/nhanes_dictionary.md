# NHANES variable dictionary (2015-2016 cycle, "I" files)

Source: https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2015/DataFiles/ (CDC/NCHS, public use).
Cycle choice: 2015-2016 is the most recent cycle that includes the dedicated
screen-time questions; the 2017-2018 cycle DROPPED PAQ710/PAQ715 (only general
sedentary minutes PAD680 remained).

| Variable | File | Meaning | Codes |
|---|---|---|---|
| SEQN | all | respondent ID (merge key) | - |
| RIAGENDR | DEMO_I | gender | 1=Male 2=Female |
| RIDAGEYR | DEMO_I | age in years | 0-79, 80+ top-coded |
| WTMEC2YR | DEMO_I | MEC examination weight (2-yr) | used for weighted analysis |
| SDMVPSU / SDMVSTRA | DEMO_I | design PSU / strata | (noted for design-based SEs) |
| SLD012 | SLQ_I | usual sleep hours on weekdays | 2-14 valid; 77/99 = refused/DK |
| SLQ050 | SLQ_I | ever told doctor had trouble sleeping? | 1=Yes 2=No |
| PAQ710 | PAQ_I | daily hours watching TV/videos (past 30 d) | 0-24; 77/99 missing |
| PAQ715 | PAQ_I | daily hours computer/games (past 30 d) | 0-24; 77/99 missing |
| PAD680 | PAQ_I | total daily sedentary minutes | 0-1320; 7777/9999 missing |

Derived: screen_hours = PAQ710 + PAQ715 (NaN if >24);
sleep_hours = SLD012 (valid 2-14 h);
analysis population: adults 18+ with complete screen+sleep+weight.
