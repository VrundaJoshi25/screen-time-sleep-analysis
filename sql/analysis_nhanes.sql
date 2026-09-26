-- Q1: average sleep and screen time by gender (GROUP BY)
SELECT gender,
       COUNT(*)              AS n,
       ROUND(AVG(sleep_hours), 2)  AS mean_sleep_h,
       ROUND(AVG(screen_hours), 2) AS mean_screen_h
FROM nhanes
WHERE sleep_hours IS NOT NULL AND screen_hours IS NOT NULL
GROUP BY gender;

-- Q2: screen-time groups built with a CTE, then summarized
WITH screen_groups AS (
  SELECT sleep_hours,
         CASE WHEN screen_hours < 2  THEN 'low (<2h)'
              WHEN screen_hours < 5  THEN 'medium (2-5h)'
              WHEN screen_hours < 8  THEN 'high (5-8h)'
              ELSE 'very high (8h+)' END AS screen_group
  FROM nhanes
  WHERE age >= 18 AND sleep_hours IS NOT NULL AND screen_hours IS NOT NULL
)
SELECT screen_group, COUNT(*) AS n, ROUND(AVG(sleep_hours), 2) AS mean_sleep_h
FROM screen_groups
GROUP BY screen_group
ORDER BY mean_sleep_h DESC;

-- Q3: window function - screen-time quartiles within gender, average sleep per quartile
SELECT gender, quartile, COUNT(*) AS n, ROUND(AVG(sleep_hours), 2) AS mean_sleep_h
FROM (
  SELECT gender, sleep_hours,
         NTILE(4) OVER (PARTITION BY gender ORDER BY screen_hours) AS quartile
  FROM nhanes
  WHERE age >= 18 AND sleep_hours IS NOT NULL AND screen_hours IS NOT NULL
)
GROUP BY gender, quartile
ORDER BY gender, quartile;
