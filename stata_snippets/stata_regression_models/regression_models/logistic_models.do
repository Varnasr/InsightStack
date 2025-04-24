* ============================================================
* logistic_models.do
* Purpose: Predict high blood pressure using logistic regression
* Input: health_survey.csv
* Output: Logit model
* ============================================================

clear all
set more off

import delimited using "health_survey.csv", clear

* Define hypertension
gen high_bp = bp_sys >= 140 | bp_dia >= 90

* Encode gender
encode gender, gen(gender_code)

* Logistic regression
logit high_bp age gender_code

* Robust SE
logit high_bp age gender_code, vce(robust)