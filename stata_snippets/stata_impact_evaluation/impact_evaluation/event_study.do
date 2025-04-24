* ============================================================
* event_study.do
* Purpose: Visualize treatment over time (mock 2-period data)
* Input: impact_eval_data.csv
* ============================================================

clear all
set more off

import delimited using "impact_eval_data.csv", clear

collapse (mean) outcome, by(time treated)

twoway (line outcome time if treated == 1, lcolor(blue)) ///
       (line outcome time if treated == 0, lcolor(red)), ///
       legend(label(1 "Treated") label(2 "Control")) ///
       title("Event Study Style Plot")