# Econometrics

Causal inference and regression methods for development research, implemented in Python and R.

## Contents

| Script | Method | Language |
|--------|--------|----------|
| `difference_in_differences.py` | DiD with parallel trends test | Python |
| `propensity_score_matching.py` | PSM with nearest-neighbor and caliper matching | Python |
| `regression_discontinuity.py` | Sharp RDD with bandwidth selection | Python |
| `instrumental_variables.py` | 2SLS estimation with diagnostics | Python |
| `sensitivity_analysis.py` | Rosenbaum bounds for causal claims | Python |
| `did_analysis.R` | DiD with event study plot | R |
| `psm_analysis.R` | PSM using MatchIt package | R |

## Sample Data

`sample_program_data.csv` contains simulated data for a development program evaluation:
- 500 observations (250 treatment, 250 control)
- Pre/post periods with outcome, covariates, and treatment assignment
- Includes a running variable for RDD examples

## Usage

```bash
# Python
pip install pandas numpy statsmodels scipy matplotlib
python difference_in_differences.py

# R
Rscript did_analysis.R
```

For Stata implementations, see `stata_snippets/stata_impact_evaluation/`.
