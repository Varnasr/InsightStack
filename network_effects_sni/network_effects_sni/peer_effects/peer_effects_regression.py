
import pandas as pd
import statsmodels.api as sm

# Load the data with added network metrics
df = pd.read_csv('../data/shg_with_network_metrics.csv')

# Normalize centrality for regression
df['eigen_centrality_norm'] = (df['eigen_centrality'] - df['eigen_centrality'].mean()) / df['eigen_centrality'].std()

# Group average savings by peer group (excluding own value)
df['peer_avg_savings'] = df.groupby('peer_group_id')['monthly_savings'].transform('mean')
df['peer_avg_savings_excl_self'] = df.apply(
    lambda row: (df[(df['peer_group_id'] == row['peer_group_id']) & (df['id'] != row['id'])]['monthly_savings'].mean())
    if len(df[df['peer_group_id'] == row['peer_group_id']]) > 1 else row['monthly_savings'], axis=1
)

# Prepare regression: own savings ~ peer average savings + controls
X = df[['peer_avg_savings_excl_self', 'age', 'education_years', 'eigen_centrality_norm']]
X = sm.add_constant(X)
y = df['monthly_savings']

# Run regression
model = sm.OLS(y, X).fit()
print(model.summary())

# Save regression results
with open('../peer_effects/peer_effects_results.txt', 'w') as f:
    f.write(model.summary().as_text())
