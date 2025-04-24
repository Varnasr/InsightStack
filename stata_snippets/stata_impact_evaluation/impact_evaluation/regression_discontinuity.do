* ============================================================
* regression_discontinuity.do
* Purpose: Estimate treatment effect at a cutoff using RDD
* Input: impact_eval_data.csv
* ============================================================

clear all
set more off

import delimited using "impact_eval_data.csv", clear

* Assume eligibility cutoff at age = 40 for program participation
gen running = age
gen treat_rdd = (age >= 40)

* Local linear regression using rdrobust (if installed) or manually
reg outcome treat_rdd running if age >= 35 & age <= 45, robust

* Optional: Graph
twoway (scatter outcome age) (lfit outcome age if age < 40) (lfit outcome age if age >= 40), ///
    title("Regression Discontinuity at Age 40")