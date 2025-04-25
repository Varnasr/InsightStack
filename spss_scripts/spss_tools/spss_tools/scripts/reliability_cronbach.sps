
* SPSS Syntax: Reliability Analysis using Cronbach's Alpha.

* Step 1: Load dataset (replace with actual path if needed).
GET FILE='we_employment_survey.sav'.

* Step 2: Assume a 4-item scale for job satisfaction (placeholder variables for demo).
* Replace with real Likert-style variables in practical use.

* For demo: simulate job satisfaction index using numeric variables.
* Variables: weekly_hours, wages, edu_level_num, age.

RELIABILITY
  /VARIABLES=weekly_hours wages edu_level_num age
  /SCALE('Job Satisfaction Index') ALL
  /MODEL=ALPHA
  /STATISTICS=DESCRIPTIVE SCALE CORR
  /SUMMARY=TOTAL.

* Output includes:
* - Cronbach's Alpha
* - Item-total statistics
* - Inter-item correlations
