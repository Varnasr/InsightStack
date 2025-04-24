* ============================================================
* master_script.do
* Purpose: Run all steps of a project from cleaning to output
* ============================================================

clear all
set more off

* Step 1: Clean health survey data
do data_management/import_cleaning.do

* Step 2: Descriptive analysis
do descriptive_analysis/summary_stats.do

* Step 3: Run regression
do regression_models/linear_regression.do

* Step 4: Export tables
do reproducibility/export_results.do

* Add more steps as needed