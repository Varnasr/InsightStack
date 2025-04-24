* ============================================================
* summary_stats.do
* Purpose: Generate summary statistics grouped by gender and district
* Input: health_survey.csv
* Output: Summary table (in log or exportable via estout)
* ============================================================

clear all
set more off

* Import dataset
import delimited using "health_survey.csv", clear

* Generate basic summary stats by district
table district, contents(mean age mean bp_sys mean bp_dia)

* By gender
table gender, contents(mean age mean bp_sys mean bp_dia)

* Optionally export using esttab or outsheet
* estpost summarize age bp_sys bp_dia
* esttab using summary_table.rtf, cells(mean sd) replace