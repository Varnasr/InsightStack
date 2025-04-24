* ============================================================
* svyset.do
* Purpose: Define survey design for sample data
* Input: health_survey.csv
* ============================================================

clear all
set more off

import delimited using "health_survey.csv", clear

* Simulate survey structure
gen psu = mod(hh_id, 10)
gen strata = cond(district=="Khunti", 1, cond(district=="Dhubri", 2, 3))
gen weight = runiform(0.8, 1.2)

* Define survey design
svyset psu [pweight=weight], strata(strata)

* Check settings
svydescribe