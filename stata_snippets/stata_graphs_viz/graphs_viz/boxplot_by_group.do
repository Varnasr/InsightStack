* ============================================================
* boxplot_by_group.do
* Purpose: Boxplot of test scores by gender and school type
* Input: education_labels.csv
* ============================================================

clear all
set more off

import delimited using "education_labels.csv", clear

graph box test_score, over(gender) title("Test Score Distribution by Gender")
graph export "boxplot_gender.png", replace

graph box test_score, over(school_type) title("Test Score Distribution by School Type")
graph export "boxplot_school_type.png", replace