
use "../sample_data/sample_data.dta", clear

* Missing values
misstable summarize

* Duplicate check
duplicates report id

* Invalid gender check
list if gender != "M" & gender != "F"
