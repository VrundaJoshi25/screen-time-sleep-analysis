-- MAIN-STUDY analysis SQL (activates when data/clean/main_study.csv exists).
-- Table name: main_study. Columns: age, gender, program_year, stratum,
-- screen_hours, screen_hours_rec, sleep_hours, sleep_quality,
-- screens_30min_bed (1/0), workload_hours, caffeine_servings, exercise_days.

-- Q1: average sleep and screen time per stratum (quota check + stratum means)
SELECT stratum,
       COUNT(*)                    AS n,
       ROUND(AVG(sleep_hours), 2)  AS mean_sleep_h,
       ROUND(AVG(screen_hours), 2) AS mean_screen_h
FROM main_study
GROUP BY stratum
ORDER BY stratum;

-- Q2: CTE - workload levels first, then sleep by workload level
WITH workload_levels AS (
  SELECT sleep_hours, screen_hours,
         CASE WHEN workload_hours < 4 THEN 'light (<4h)'
              WHEN workload_hours < 8 THEN 'moderate (4-8h)'
              ELSE 'heavy (8h+)' END AS workload_level
  FROM main_study
)
SELECT workload_level, COUNT(*) AS n,
       ROUND(AVG(sleep_hours), 2) AS mean_sleep_h,
       ROUND(AVG(screen_hours), 2) AS mean_screen_h
FROM workload_levels
GROUP BY workload_level
ORDER BY mean_sleep_h DESC;

-- Q3: window function - screen-time quartile within each stratum vs sleep
SELECT stratum, screen_quartile, COUNT(*) AS n, ROUND(AVG(sleep_hours), 2) AS mean_sleep_h
FROM (
  SELECT stratum, sleep_hours,
         NTILE(4) OVER (PARTITION BY stratum ORDER BY screen_hours) AS screen_quartile
  FROM main_study
)
GROUP BY stratum, screen_quartile
ORDER BY stratum, screen_quartile;

-- Q4: bonus - pre-bed screen users vs non-users
SELECT screens_30min_bed, COUNT(*) AS n, ROUND(AVG(sleep_hours), 2) AS mean_sleep_h
FROM main_study
GROUP BY screens_30min_bed;
