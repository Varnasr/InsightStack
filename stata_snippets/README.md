## 📂 Repository Structure: Folder-by-Folder

This repository is organized by functional workflow. Each folder contains complete `.do` files and simulated Indian datasets. All code is runnable and documented for clarity and reproducibility.

| Folder               | Description                                              | Scripts Inside                                  | Dataset(s) Used                |
|----------------------|----------------------------------------------------------|------------------------------------------------|--------------------------------|
| `data_management/`   | Data import, cleaning, merge, and labeling               | `import_cleaning.do`, `merge_append.do`, ...   | `health_survey.csv`, ...       |
| `descriptive_analysis/` | Summary statistics, cross-tabulations, ...            | `summary_stats.do`, ...                        | `education_labels.csv`, ...    |
| `regression_models/` | OLS, logistic, DiD, clustered SEs                        | `ols_example.do`, `did_clustered.do`, ...      | `baseline_endline.dta`, ...    |
| `visualization/`     | Equity graphs, dot plots, maps                           | `dotplot.do`, `eq_plot.do`, ...                | `education_labels.csv`, ...    |
| `graphs_viz/`        | Stacked bar, boxplot, panel chart                        | `stacked.do`, `panel_viz.do`                   | `school_panel.dta`, ...        |
| `templates/`         | Standard templates for Stata projects                    | `project_template.do`, `clean_labels.do`       | Dummy/example only             |
