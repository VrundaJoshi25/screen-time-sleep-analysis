"""
Sleep Project - Data preparation
Source: Student Insomnia and Educational Outcomes Dataset (Mendeley Data,
DOI 10.17632/5mvrx4v62z.2, CC BY 4.0, Daffodil International University,
survey Oct-Nov 2024, n=996 students).

Builds the coded analysis dataset:
  - ordinal codes for frequency/stress/quality questions
  - midpoint hours for the sleep-duration ranges
Outputs: analysis_data.csv, codebook.txt, first_results.txt
"""
import pandas as pd
import numpy as np
from scipy import stats

import os
FOLDER = os.path.dirname(os.path.abspath(__file__)) + os.sep
df = pd.read_csv(FOLDER + "student_insomnia_raw.csv")

# ---------------- column map (short names) ----------------
COLS = {
    '1. What is your year of study?': 'year',
    '2. What is your gender?': 'gender',
    '3. How often do you have difficulty falling asleep at night? ': 'insomnia_freq',
    '4. On average, how many hours of sleep do you get on a typical day?': 'sleep_cat',
    '5. How often do you wake up during the night and have trouble falling back asleep?': 'awakenings_freq',
    '6. How would you rate the overall quality of your sleep?': 'sleep_quality_cat',
    '7. How often do you experience difficulty concentrating during lectures or studying due to lack of sleep?': 'concentration_freq',
    '8. How often do you feel fatigued during the day, affecting your ability to study or attend classes?': 'fatigue_freq',
    '9. How often do you miss or skip classes due to sleep-related issues (e.g., insomnia, feeling tired)?': 'skip_classes_freq',
    '10. How would you describe the impact of insufficient sleep on your ability to complete assignments and meet deadlines?': 'deadline_impact_cat',
    '11. How often do you use electronic devices (e.g., phone, computer) before going to sleep?': 'screen_freq_cat',
    '12. How often do you consume caffeine (coffee, energy drinks) to stay awake or alert?': 'caffeine_freq_cat',
    '13. How often do you engage in physical activity or exercise?': 'activity_freq_cat',
    '14. How would you describe your stress levels related to academic workload?': 'stress_cat',
    '15. How would you rate your overall academic performance (GPA or grades) in the past semester?': 'performance_cat',
}
d = df.rename(columns=COLS).drop(columns=['Timestamp'])

# ---------------- coding maps ----------------
FREQ5 = {'Never': 1, 'Rarely (1-2 times a week)': 2, 'Sometimes (3-4 times a week)': 3,
         'Often (5-6 times a week)': 4, 'Every night': 5, 'Every day': 5,
         'Sometimes': 3, 'Often': 4, 'Rarely': 2, 'Always': 5,
         'Sometimes (1-2 times a week)': 3, 'Rarely (1-2 times a month)': 2,
         'Often (3-4 times a week)': 4}
SLEEP_MID = {'Less than 4 hours': 3.0, '4-5 hours': 4.5, '6-7 hours': 6.5,
             '7-8 hours': 7.5, 'More than 8 hours': 8.5}
SLEEP_ORD = {'Less than 4 hours': 1, '4-5 hours': 2, '6-7 hours': 3,
             '7-8 hours': 4, 'More than 8 hours': 5}
QUALITY = {'Very poor': 1, 'Poor': 2, 'Average': 3, 'Good': 4, 'Very good': 5}
STRESS = {'No stress': 1, 'Low stress': 2, 'High stress': 3, 'Extremely high stress': 4}
IMPACT = {'No impact': 1, 'Minor impact': 2, 'Moderate impact': 3,
          'Major impact': 4, 'Severe impact': 5}
PERF = {'Poor': 1, 'Below Average': 2, 'Average': 3, 'Good': 4, 'Excellent': 5}

d['screen_freq'] = d['screen_freq_cat'].map(FREQ5)
d['sleep_hours'] = d['sleep_cat'].map(SLEEP_MID)
d['sleep_ord'] = d['sleep_cat'].map(SLEEP_ORD)
d['caffeine'] = d['caffeine_freq_cat'].map(FREQ5)
d['activity'] = d['activity_freq_cat'].map(FREQ5)
d['stress'] = d['stress_cat'].map(STRESS)
d['sleep_quality'] = d['sleep_quality_cat'].map(QUALITY)
d['insomnia'] = d['insomnia_freq'].map(FREQ5)
d['awakenings'] = d['awakenings_freq'].map(FREQ5)
d['concentration'] = d['concentration_freq'].map(FREQ5)
d['fatigue'] = d['fatigue_freq'].map(FREQ5)
d['skip_classes'] = d['skip_classes_freq'].map(FREQ5)
d['deadline_impact'] = d['deadline_impact_cat'].map(IMPACT)
d['performance'] = d['performance_cat'].map(PERF)

assert d[['screen_freq', 'sleep_hours', 'caffeine', 'activity', 'stress']].notna().all().all(), "coding failed"

d.to_csv(FOLDER + "analysis_data.csv", index=False)

# ---------------- codebook ----------------
codebook = """CODEBOOK - analysis_data.csv  (n = %d students)
Source: Mendeley Data DOI 10.17632/5mvrx4v62z.2 (CC BY 4.0)

IDENTIFIERS / DEMOGRAPHICS
  year                First year | Second year | Third year | Graduate student
  gender              Male | Female

KEY VARIABLES (coded)
  screen_freq_cat     original label: how often devices used before sleep
  screen_freq         1=Never 2=Rarely(1-2/wk) 3=Sometimes(3-4/wk) 4=Often(5-6/wk) 5=Every night
  sleep_cat           original label: average hours of sleep per day
  sleep_ord           1=<4h 2=4-5h 3=6-7h 4=7-8h 5=>8h
  sleep_hours         midpoint of range: 3.0, 4.5, 6.5, 7.5, 8.5
  caffeine            1=Never ... 5=Every day   (caffeine to stay awake/alert)
  activity            1=Never ... 5=Every day   (physical activity/exercise)
  stress              1=No 2=Low 3=High 4=Extremely high  (academic-workload stress)

SECONDARY (coded the same way)
  insomnia, awakenings, concentration, fatigue, skip_classes  1..5 frequency
  sleep_quality       1=Very poor .. 5=Very good
  deadline_impact     1=No impact .. 5=Severe impact
  performance         1=Poor .. 5=Excellent (self-rated last semester)

NOTES
  - All variables are self-reported survey answers (single sitting, retrospective).
  - sleep_hours is an approximation (range midpoints); sleep_ord keeps the original
    ordinal information for rank-based methods.
""" % len(d)
open(FOLDER + "codebook.txt", "w", encoding="utf-8").write(codebook)

# ---------------- first real results ----------------
out = []
out.append("CLEAN ANALYSIS DATASET: n = %d, %d columns" % (d.shape[0], d.shape[1]))
out.append("Missing values: %d | Full duplicates: %d\n" % (d.isna().sum().sum(), d.duplicated().sum()))

ct = pd.crosstab(d['screen_freq_cat'], d['sleep_cat'])
order_s = ['Never', 'Rarely (1-2 times a week)', 'Sometimes (3-4 times a week)',
           'Often (5-6 times a week)', 'Every night']
order_h = ['Less than 4 hours', '4-5 hours', '6-7 hours', '7-8 hours', 'More than 8 hours']
ct = ct.reindex(index=order_s, columns=order_h)
out.append("CROSS-TAB: device use before sleep (rows) x sleep duration (cols), counts")
out.append(ct.to_string())

grp = d.groupby('screen_freq')['sleep_hours'].agg(['count', 'mean', 'std']).round(3)
out.append("\nMEAN sleep_hours (midpoint) by screen-use frequency:")
out.append(grp.to_string())

rho, p = stats.spearmanr(d['screen_freq'], d['sleep_hours'])
out.append("\nSpearman rho(screen_freq, sleep_hours) = %.4f  (p = %.4g)" % (rho, p))
rhoq, pq = stats.spearmanr(d['screen_freq'], d['sleep_quality'])
out.append("Spearman rho(screen_freq, sleep_quality) = %.4f  (p = %.4g)" % (rhoq, pq))
kt = stats.kruskal(*[g['sleep_hours'].values for _, g in d.groupby('screen_freq')])
out.append("Kruskal-Wallis across the 5 screen groups: H = %.2f, p = %.4g" % (kt.statistic, kt.pvalue))

txt = "\n".join(out)
open(FOLDER + "first_results.txt", "w", encoding="utf-8").write(txt)
print(txt)
