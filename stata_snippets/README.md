---

## 📂 Repository Structure: Folder-by-Folder

This repository is organized by functional workflow. Each folder contains complete `.do` files and simulated Indian datasets. All code is runnable and documented for clarity and reproducibility.

| Folder | Description | Scripts Inside | Dataset(s) Used |
|--------|-------------|----------------|-----------------|
| `data_management/` | Data import, cleaning, merge, and labeling | `import_cleaning.do`, `merge_append.do`, `label_rename.do` | `health_survey.csv`, `livelihoods_panel.csv`, `education_labels.csv` |
| `descriptive_analysis/` | Summary statistics, cross-tabulations, and missing value reports | `summary_stats.do`, `tabulations.do`, `missing_values.do` | `education_labels.csv`, `health_survey.csv` |
| `regression_models/` | Linear/logistic models, panel regressions, and clustered SEs | `linear_regression.do`, `logistic_models.do`, `fixed_effects_panel.do`, `clustered_se.do` | All 3 datasets |
| `graphs_viz/` | Bar charts, histograms, boxplots, dot plots, line/panel graphs | `bar_histogram.do`, `boxplot_by_group.do`, `scatter_line.do`, `panel_line_income.do`, etc. | All 3 datasets |
| `survey_analysis/` | Survey design setup and weighted estimates using `svy:` | `svyset.do`, `weighted_means.do`, `design_effects.do` | `health_survey.csv` |
| `impact_evaluation/` | DiD, propensity score matching, event study, IV (LATE), and MDE | `diff_in_diff.do`, `propensity_score_matching.do`, `event_study.do`, `itt_late_estimation.do`, `mde_power_calc.do` | `impact_eval_data.csv` |
| `reproducibility/` | Master script, project structure template, and result exports | `master_script.do`, `export_results.do`, `project_structure_template.txt` | `education_labels.csv` |
| `templates/` | Reusable skeletons and annotated starter files | `annotated_do_file.do`, `project_folder_template.zip` | – |

---

## 🗂 About the Template Files

The `templates/` folder includes fully-commented starter files and a zipped project layout to help users begin structured Stata workflows. These are not blank files or trivial placeholders — they are scaffolds to support program teams, researchers, and evaluation professionals in creating reproducible outputs.

---

## 🔄 All Code is Executable

Each `.do` file in this repository is:
- Written with real logic and flow
- Paired with working synthetic datasets
- Safe to reuse or build upon

Use it to teach, test, prototype, or document — all content is designed for real-world utility in public health, gender, WEE, education, livelihoods, and climate-focused projects.

---

## 📌 Supplementary Files

- 📘 [design_coverage.md](./design_coverage.md) — Full list of research designs covered by this repository, with links to examples.
- 🧭 [ROADMAP.md](./ROADMAP.md) — Planned expansions, advanced methods (e.g., block randomization, synthetic controls), and ideas for contributors.

These documents help contextualize what's already included and what's coming next.

---
