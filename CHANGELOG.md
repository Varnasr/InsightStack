# InsightStack Changelog

All notable changes to InsightStack are documented here.

---

## [v1.3.0] - 2025-04-28

### Added
- `econometrics/` module fully built with 7 implementations:
  - `difference_in_differences.py` — DiD estimation with parallel trends test, covariate controls, and visualization
  - `propensity_score_matching.py` — PSM with nearest-neighbor matching, balance assessment, and ATT estimation
  - `regression_discontinuity.py` — Sharp RDD with bandwidth selection, McCrary density test, and visualization
  - `instrumental_variables.py` — 2SLS estimation with first-stage F-test diagnostics
  - `sensitivity_analysis.py` — Rosenbaum bounds, placebo tests, permutation inference
  - `did_analysis.R` — DiD in R with event study plot using ggplot2
  - `psm_analysis.R` — PSM in R using MatchIt package with balance diagnostics
- `econometrics/sample_program_data.csv` — 20-row simulated program evaluation dataset

### Improved
- README updated: econometrics module status changed from Planned to Ready

## [v1.2.0] - 2025-04-24

### Added
- `impact_evaluation/`: DiD, propensity score matching, ITT/LATE estimation, event study, MDE power calculation
- `regression_discontinuity.do` and `heterogeneous_effects.do` for causal inference
- GitHub Action for automatic changelog generation
- `ROADMAP.md` and `design_coverage.md`

### Improved
- `graphs_viz/`: added boxplot_by_group, panel_line_income, combine_graphs
- README enhancements with badges and ecosystem links

## [v1.1.0] - 2025-04-20

### Added
- Core data folders: `data_management/`, `descriptive_analysis/`, `regression_models/`
- Templates: `annotated_do_file.do`, `project_folder_template.zip`
- Synthetic datasets: `education_labels.csv`, `livelihoods_panel.csv`, `health_survey.csv`

### Fixed
- Label inconsistencies in `logistic_models.do`
- Folder alignment and README formatting

## [v1.0.0] - 2025-04-18

### Initial Release
- Project bootstrapped with InsightStack architecture
- GitHub Pages, README, and folder layout
