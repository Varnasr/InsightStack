# Replication Folder (InsightStack)

This folder allows replication of a simple linear regression analysis using synthetic data.

## Folder Structure:
- `data/simulated_study_data.csv` – synthetic dataset (100 rows)
- `scripts/run_regression.py` – Python script using `statsmodels`
- `scripts/run_regression.R` – R script using `lm()`
- `output/` – regression result summaries will be saved here

## How to Use
1. Run either script inside `scripts/`.
2. Check `output/` for results.
3. Modify or reuse this structure for your own replications.

This structure supports transparent, reproducible workflows.