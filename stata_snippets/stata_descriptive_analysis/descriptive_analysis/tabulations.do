* ============================================================
* tabulations.do
* Purpose: Generate frequency tables and cross-tabs
* Input: education_labels.csv
* Output: Cross-tab results
* ============================================================

clear all
set more off

import delimited using "education_labels.csv", clear

* Cross-tab of gender vs grade
tab gender grade_level, row col

* School type vs performance group
gen performance = .
replace performance = 1 if test_score < 40
replace performance = 2 if test_score >= 40 & test_score < 60
replace performance = 3 if test_score >= 60

label define perf 1 "Low" 2 "Average" 3 "High"
label values performance perf

tab school_type performance, col chi2