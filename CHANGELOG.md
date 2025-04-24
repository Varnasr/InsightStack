# 📑 InsightStack – Changelog

All major changes to the InsightStack repository will be documented here.  
This file is auto-updated via GitHub Actions on each push to `main`.

---

## [v1.2.0] – 2025-04-24

### ✨ Added
- `impact_evaluation/`: full folder with `diff_in_diff.do`, `propensity_score_matching.do`, `itt_late_estimation.do`, `event_study.do`, and `mde_power_calc.do`
- `regression_discontinuity.do` and `heterogeneous_effects.do` for causal inference
- GitHub Action for automatic changelog generation
- `ROADMAP.md` and `design_coverage.md` with forward-looking methodology structure

### 🛠 Improved
- `graphs_viz/`: added `boxplot_by_group`, `panel_line_income`, and `combine_graphs.do`
- `README.md` enhancements with badge-ready layout and external links

---

## [v1.1.0] – 2025-04-20

### ✨ Added
- Core data folders: `data_management/`, `descriptive_analysis/`, `regression_models/`
- Templates: `annotated_do_file.do`, `project_folder_template.zip`
- Complete synthetic datasets: `education_labels.csv`, `livelihoods_panel.csv`, `health_survey.csv`

### 🧹 Fixed
- Label inconsistencies in `logistic_models.do`
- Folder alignment and README formatting

---

## [v1.0.0] – 2025-04-18

### 🎉 Initial Release
- Project bootstrapped with InsightStack architecture
- Setup for GitHub Pages, README footer, and folder layout finalized