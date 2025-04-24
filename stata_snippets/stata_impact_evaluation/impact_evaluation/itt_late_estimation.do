* ============================================================
* itt_late_estimation.do
* Purpose: Estimate ITT and LATE using eligibility as instrument
* Input: impact_eval_data.csv
* ============================================================

clear all
set more off

import delimited using "impact_eval_data.csv", clear

* ITT: effect of being eligible
reg outcome eligible, robust

* LATE: use eligibility as IV for treatment
ivregress 2sls outcome (treated = eligible), robust