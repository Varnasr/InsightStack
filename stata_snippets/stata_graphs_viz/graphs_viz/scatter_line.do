* ============================================================
* scatter_line.do
* Purpose: Create scatter and line plots
* Inputs: health_survey.csv, livelihoods_panel.csv
* Output: Graphs
* ============================================================

clear all
set more off

* Scatterplot: Systolic vs. Diastolic BP
import delimited using "health_survey.csv", clear
scatter bp_sys bp_dia, title("Systolic vs Diastolic BP")

* Line plot: Household income over time
import delimited using "livelihoods_panel.csv", clear
collapse (mean) income, by(year)
line income year, title("Average Household Income Over Time")