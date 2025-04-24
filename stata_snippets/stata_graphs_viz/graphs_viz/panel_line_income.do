* ============================================================
* panel_line_income.do
* Purpose: Panel chart of income over time by district
* Input: livelihoods_panel.csv
* ============================================================

clear all
set more off

import delimited using "livelihoods_panel.csv", clear

collapse (mean) income, by(district year)

twoway (line income year if district=="Kurnool", lcolor(blue)) ///
       (line income year if district=="Khunti", lcolor(red)), ///
       legend(label(1 "Kurnool") label(2 "Khunti")) ///
       title("Income Over Time by District")

graph export "income_panel_district.png", replace