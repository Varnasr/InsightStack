* ============================================================
* export_results.do
* Purpose: Export results using esttab or outsheet
* ============================================================

clear all
set more off

import delimited using "education_labels.csv", clear

encode gender, gen(gender_code)
encode school_type, gen(school_code)

regress test_score gender_code school_code

* Save regression output
estimates store mymodel

* Export with esttab (if installed)
* esttab mymodel using outputs/tables/reg_output.rtf, replace se label title("OLS Test Score Regression")

* Simple CSV export of descriptive stats
summarize test_score, detail
outsheet using outputs/tables/testscore_summary.csv, replace