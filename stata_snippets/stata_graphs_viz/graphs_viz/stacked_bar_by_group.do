* ============================================================
* stacked_bar_by_group.do
* Purpose: Stacked bar chart of performance categories by school type
* Input: education_labels.csv
* ============================================================

clear all
set more off

import delimited using "education_labels.csv", clear

gen performance = .
replace performance = 1 if test_score < 40
replace performance = 2 if test_score >= 40 & test_score < 60
replace performance = 3 if test_score >= 60

label define perf 1 "Low" 2 "Average" 3 "High"
label values performance perf

graph bar (count), over(school_type) over(performance) stack ///
    title("Performance by School Type")
graph export "stacked_bar_performance_school.png", replace