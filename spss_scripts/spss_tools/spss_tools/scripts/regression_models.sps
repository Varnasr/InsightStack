
* SPSS Syntax: Regression Models for Women's Employment Dataset.

* Step 1: Load the data file (path to be edited if using GUI).
GET FILE='we_employment_survey.sav'.

* Step 2: Descriptive statistics for variables used in models.
DESCRIPTIVES VARIABLES=age edu_level_num weekly_hours wages.

* Step 3: Linear regression: Predicting wages.
REGRESSION
  /DEPENDENT wages
  /METHOD=ENTER age edu_level_num weekly_hours
  /STATISTICS=COEFF OUTS R ANOVA COLLIN TOL VIF
  /SCATTERPLOT=(*ZRESID , *ZPRED)
  /RESIDUALS HISTOGRAM(ZRESID) NORMPROB(ZRESID).

* Step 4: Logistic regression: Predicting formal sector employment.
LOGISTIC REGRESSION VARIABLES formal_sector
  /METHOD=ENTER age edu_level_num weekly_hours
  /CRITERIA=PIN(.05) POUT(.10) ITERATE(20)
  /CLASSPLOT
  /PRINT=CI(95) GOODFIT
  /SAVE=PRED(pr_formal) PROB.

* Step 5: Post-model evaluation.
FREQUENCIES VARIABLES=formal_sector pr_formal.
