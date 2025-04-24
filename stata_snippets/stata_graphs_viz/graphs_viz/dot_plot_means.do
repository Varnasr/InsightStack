* ============================================================
* dot_plot_means.do
* Purpose: Dot plot showing mean scores by school type
* Input: education_labels.csv
* ============================================================

clear all
set more off

import delimited using "education_labels.csv", clear

collapse (mean) test_score, by(school_type)

graph dot test_score, over(school_type) ///
    title("Mean Test Scores by School Type")
graph export "dot_plot_scores_school.png", replace