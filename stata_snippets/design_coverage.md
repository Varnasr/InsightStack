# 🧪 Research Designs Covered in This Repository

This repository includes working Stata scripts and datasets aligned to multiple real-world research designs commonly used in evaluation, development economics, and applied social science.

## ✅ Design Types and Coverage

| Design Type | Folder | Script(s) | Description |
|-------------|--------|-----------|-------------|
| **Cross-sectional** | `data_management/`, `descriptive_analysis/`, `regression_models/` | `summary_stats.do`, `linear_regression.do` | Uses static datasets to perform basic summaries and regression |
| **Panel/Longitudinal** | `data_management/`, `regression_models/`, `graphs_viz/` | `merge_append.do`, `fixed_effects_panel.do`, `panel_line_income.do` | Multi-period household income data modeled with FE + panel visual |
| **RCT: Treatment vs Control** | `impact_evaluation/` | `diff_in_diff.do`, `itt_late_estimation.do` | Simulated RCT with treatment × time and ITT/LATE logic |
| **Baseline vs Endline** | `impact_evaluation/` | `diff_in_diff.do`, `event_study.do` | Simulated pre-post evaluation for outcomes and trends |
| **Quasi-experimental (PSM)** | `impact_evaluation/` | `propensity_score_matching.do` | Uses `teffects psmatch` to estimate treatment effect on matched pairs |
| **Instrumental Variable (LATE)** | `impact_evaluation/` | `itt_late_estimation.do` | Uses an eligibility rule as an instrument for treatment assignment |
| **Minimum Detectable Effect (MDE)** | `impact_evaluation/` | `mde_power_calc.do` | Power analysis to calculate sample size or detectable effect |
| **Event Study Visualization** | `impact_evaluation/` | `event_study.do` | Displays differential outcome trends across treated and control groups |

---

## 📌 All scripts are paired with synthetic, simulated Indian datasets and annotated for clarity and reproducibility.

For questions or extensions (e.g., RDD, synthetic controls), please open an issue or contact the repository author.