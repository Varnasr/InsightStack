
* SPSS Syntax: Summary Statistics for Education Dataset.
GET FILE='education_outcomes_by_gender.sav'.
FREQUENCIES VARIABLES=gender caste district /STATISTICS=MODE.
DESCRIPTIVES VARIABLES=grade_achieved /STATISTICS=MEAN STDDEV MIN MAX.
CROSSTABS /TABLES=gender BY caste /FORMAT=AVALUE TABLES /STATISTICS=CHISQ.
