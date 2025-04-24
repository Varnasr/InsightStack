* ============================================================
* missing_values.do
* Purpose: Identify missing values and summarize
* Input: health_survey.csv and education_labels.csv
* Output: Log or list of variables with missing values
* ============================================================

clear all
set more off

* Health dataset
import delimited using "health_survey.csv", clear
display "Health dataset missing value summary:"
misstable summarize

* Education dataset
import delimited using "education_labels.csv", clear
display "Education dataset missing value summary:"
misstable summarize