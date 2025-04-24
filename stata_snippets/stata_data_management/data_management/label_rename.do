* ============================================================
* label_rename.do
* Purpose: Label variables and clean up education data
* Input: education_labels.csv
* Output: education_cleaned.dta
* ============================================================

clear all
set more off

import delimited using "education_labels.csv", clear

* Rename for clarity
rename grade_level class
rename test_score score

* Label variables
label variable student_id "Student Identifier"
label variable class "Grade Level"
label variable gender "Gender of Student"
label variable score "Standardized Test Score"
label variable school_type "Type of School"

* Encode strings to factors
encode gender, gen(gender_code)
encode school_type, gen(school_code)

* Drop originals
drop gender school_type
rename gender_code gender
rename school_code school_type

* Save output
save "education_cleaned.dta", replace