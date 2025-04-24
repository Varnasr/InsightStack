* ============================================================
* File: annotated_do_file.do
* Author: Your Name
* Project: [Insert Project Title]
* Description:
*   This is a template for structured and readable Stata do-files.
*   It includes clear sections, variable naming, logging, labeling,
*   and modular scripting for reproducibility.
* ============================================================

* --- Project setup ---
clear all
set more off
set linesize 80

* Log file
log using logs/sample_logfile.log, replace

* --- Load Data ---
* Make sure data path is relative (assumes working dir is project root)
use "data/processed/your_clean_data.dta", clear

* --- Generate Variables ---
* Example: Create a normalized index variable
gen index_var = var1 + var2 + var3
egen z_index = std(index_var)

* --- Recode, Rename, Relabel ---
recode gender (1 = 0 "Male") (2 = 1 "Female"), gen(female)
rename var1 income
label variable income "Monthly Income (INR)"

* --- Summary Statistics ---
summarize age income z_index
tabulate gender, missing

* --- Regression Example ---
regress outcome_var income age female
estimates store model1

* --- Export Output (example) ---
* Uncomment below if using estout
* esttab model1 using outputs/tables/model1_results.rtf, replace se title("OLS")

* --- End ---
log close