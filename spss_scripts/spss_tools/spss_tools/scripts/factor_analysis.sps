
* SPSS Syntax: Exploratory Factor Analysis on Employment Survey.

* Step 1: Load the dataset.
GET FILE='we_employment_survey.sav'.

* Step 2: Assume these variables are part of a Likert-style module on work conditions or empowerment.
* For demonstration, we'll reuse some numeric variables.
* NOTE: In real usage, replace with items like q1 to q10 from a work conditions scale.

FACTOR
  /VARIABLES=weekly_hours wages edu_level_num age
  /MISSING=LISTWISE
  /ANALYSIS=weekly_hours wages edu_level_num age
  /PRINT=INITIAL EXTRACTION ROTATION
  /PLOT=EIGEN
  /CRITERIA=FACTORS(1) ITERATE(25)
  /EXTRACTION=PRINCIPAL
  /CRITERIA=EIGEN(.95)
  /ROTATION=VARIMAX
  /METHOD=CORRELATION.

* Step 3: Save factor scores (optional if used for further regression).
FACTOR
  /VARIABLES=weekly_hours wages edu_level_num age
  /MISSING=LISTWISE
  /EXTRACTION=PRINCIPAL
  /ROTATION=VARIMAX
  /SAVE REG(ALL)
  /METHOD=CORRELATION.
