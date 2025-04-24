* ============================================================
* weighted_means.do
* Purpose: Estimate weighted means using survey design
* Input: health_survey.csv
* ============================================================

clear all
set more off

import delimited using "health_survey.csv", clear

gen psu = mod(hh_id, 10)
gen strata = cond(district=="Khunti", 1, cond(district=="Dhubri", 2, 3))
gen weight = runiform(0.8, 1.2)

svyset psu [pweight=weight], strata(strata)

* Estimate weighted mean BP and age
svy: mean bp_sys bp_dia age