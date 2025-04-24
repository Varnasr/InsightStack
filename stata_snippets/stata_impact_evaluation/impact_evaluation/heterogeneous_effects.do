* ============================================================
* heterogeneous_effects.do
* Purpose: Estimate treatment heterogeneity by gender and income level
* Input: impact_eval_data.csv
* ============================================================

clear all
set more off

import delimited using "impact_eval_data.csv", clear

* Simulate subgroups
gen high_income = income > 6000
gen female = mod(hh_id, 2)

* Interaction term
gen treat_female = treated * female
gen treat_income = treated * high_income

* Regress with interactions
reg outcome treated female high_income treat_female treat_income, robust