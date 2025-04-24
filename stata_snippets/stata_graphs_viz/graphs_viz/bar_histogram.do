* ============================================================
* bar_histogram.do
* Purpose: Create bar and histogram charts
* Input: education_labels.csv
* Output: Graphs
* ============================================================

clear all
set more off

import delimited using "education_labels.csv", clear

* Bar chart: school type
graph bar (count), over(school_type) title("Student Count by School Type")

* Histogram: test score
histogram test_score, width(5) color(blue) title("Distribution of Test Scores")