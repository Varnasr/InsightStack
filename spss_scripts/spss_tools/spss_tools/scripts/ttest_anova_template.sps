
* SPSS Syntax: T-Test and One-Way ANOVA Examples for WEE Dataset.

* Step 1: Load the dataset.
GET FILE='we_employment_survey.sav'.

* Step 2: T-Test: Compare mean wages by formal vs informal sector.
T-TEST GROUPS=formal_sector(0 1)
/VARIABLES=wages
/CRITERIA=CI(.95).

* Step 3: One-way ANOVA: Compare wages by education level.
ONEWAY wages BY edu_level_num
  /STATISTICS DESCRIPTIVES
  /MISSING ANALYSIS
  /POSTHOC=TUKEY ALPHA(0.05).

* Step 4: Means and confidence intervals by education level.
MEANS TABLES=wages BY edu_level_num
  /CELLS MEAN COUNT STDDEV MIN MAX SEMEAN.

* Notes:
* - formal_sector must be coded as 0 and 1.
* - edu_level_num must be numeric ordinal: 1=Primary, ..., 4=Graduate.
