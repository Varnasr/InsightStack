* ============================================================
* linear_regression.do
* Purpose: Run OLS regression on student test scores
* Input: education_labels.csv
* Output: OLS model output
* ============================================================

clear all
set more off

import delimited using "education_labels.csv", clear

* Recode predictors
encode school_type, gen(school)
encode gender, gen(gender_code)

* Run regression
regress test_score school gender_code

* Add robust standard errors
regress test_score school gender_code, robust