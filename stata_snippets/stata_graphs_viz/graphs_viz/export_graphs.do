* ============================================================
* export_graphs.do
* Purpose: Save graphs to external files
* Inputs: education_labels.csv
* Output: PNG exports
* ============================================================

clear all
set more off

import delimited using "education_labels.csv", clear

* Histogram
histogram test_score, title("Histogram of Test Scores")
graph export "histogram_scores.png", replace

* Bar graph
graph bar (count), over(school_type) title("Students by School Type")
graph export "bar_school_type.png", replace