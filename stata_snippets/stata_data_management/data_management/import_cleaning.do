* ============================================================
* import_cleaning.do
* Purpose: Import, inspect, clean and save a survey dataset
* Input: health_survey.csv
* Output: health_cleaned.dta
* ============================================================

clear all
set more off

* Import dataset
import delimited using "health_survey.csv", clear

* Check structure
describe
summarize

* Create new variables
gen bp_diff = bp_sys - bp_dia
gen age_group = .
replace age_group = 1 if age < 30
replace age_group = 2 if age >= 30 & age < 50
replace age_group = 3 if age >= 50

label define agegrp 1 "18–29" 2 "30–49" 3 "50+"
label values age_group agegrp

* Check for missing data
misstable summarize

* Save cleaned file
save "health_cleaned.dta", replace