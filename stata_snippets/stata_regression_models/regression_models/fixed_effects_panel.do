* ============================================================
* fixed_effects_panel.do
* Purpose: Panel regression on household income with FE
* Input: livelihoods_panel.csv
* Output: FE model output
* ============================================================

clear all
set more off

import delimited using "livelihoods_panel.csv", clear

* xtset
xtset hh_id year

* Fixed effects model
xtreg income scheme_participation, fe

* Cluster-robust SE
xtreg income scheme_participation, fe vce(cluster hh_id)