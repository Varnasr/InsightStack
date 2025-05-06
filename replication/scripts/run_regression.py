import pandas as pd
import statsmodels.api as sm

df = pd.read_csv('../data/simulated_study_data.csv')
X = df[['treatment', 'age', 'income']]
X = sm.add_constant(X)
y = df['outcome']

model = sm.OLS(y, X).fit()
with open('../output/results_python.txt', 'w') as f:
    f.write(model.summary().as_text())