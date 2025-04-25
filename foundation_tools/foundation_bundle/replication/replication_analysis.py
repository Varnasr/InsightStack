# Example replication analysis in Python (replace with your own model)
import pandas as pd
import statsmodels.api as sm

df = pd.read_csv('we_employment_survey_clean.csv')
X = df[['age', 'edu_level_num', 'weekly_hours']]
X = sm.add_constant(X)
y = df['wages']

model = sm.OLS(y, X).fit()
print(model.summary())