* ============================================================
* clustered_se.do
* Purpose: Show how to run regressions with cluster-robust SE
* Input: education_labels.csv
* ============================================================

clear all
set more off

import delimited using "education_labels.csv", clear

encode school_type, gen(school)
encode gender, gen(gender_code)

gen cluster = mod(student_id, 5)

regress test_score school gender_code, vce(cluster cluster)