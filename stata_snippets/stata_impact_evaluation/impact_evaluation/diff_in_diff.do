* ============================================================
* diff_in_diff.do
* Purpose: Difference-in-Differences estimation
* Input: impact_eval_data.csv
* ============================================================

clear all
set more off

import delimited using "impact_eval_data.csv", clear

gen post = time
gen treat_group = treated
gen interaction = post * treat_group

reg outcome post treat_group interaction, robust

* Difference-in-Differences estimate = coefficient on interaction