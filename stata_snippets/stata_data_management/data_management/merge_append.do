* ============================================================
* merge_append.do
* Purpose: Merge panel data across years
* Input: livelihoods_panel.csv
* Output: merged_panel.dta
* ============================================================

clear all
set more off

* Import panel data
import delimited using "livelihoods_panel.csv", clear

* Encode string vars if needed
encode district, gen(dist_id)
drop district
rename dist_id district

* Sort and save as baseline
keep if year == 2022
sort hh_id
save "base.dta", replace

* Import again for endline
import delimited using "livelihoods_panel.csv", clear
keep if year == 2023
sort hh_id
save "end.dta", replace

* Merge
merge 1:1 hh_id using "base.dta"

* Check merge result
tab _merge

* Save merged data
save "merged_panel.dta", replace