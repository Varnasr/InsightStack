* ============================================================
* design_effects.do
* Purpose: Check design effects for key indicators
* Input: health_survey.csv
* ============================================================

clear all
set more off

import delimited using "health_survey.csv", clear

gen psu = mod(hh_id, 10)
gen strata = cond(district=="Khunti", 1, cond(district=="Dhubri", 2, 3))
gen weight = runiform(0.8, 1.2)

svyset psu [pweight=weight], strata(strata)

* Check design effect
svy: mean age

* Estimate design effect explicitly
svyset, show