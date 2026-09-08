
* SPSS Syntax: Regression Diagnostics for Wage Model.

* Step 1: Load dataset.
GET FILE='we_employment_survey.sav'.

* Step 2: Run regression with diagnostics.
REGRESSION
  /DEPENDENT wages
  /METHOD=ENTER age edu_level_num weekly_hours
  /STATISTICS=COEFF R ANOVA COLLIN TOL VIF CI(95)
  /RESIDUALS HISTOGRAM(ZRESID) NORMPROB(ZRESID) OUTLIERS
  /SCATTERPLOT(*ZPRED,*ZRESID)
  /SAVE RESID(ZRES) PRED(ZPRED) DFBETA DFFIT COOK LEVER.

* Step 3: Examine saved values for outliers and influence.
DESCRIPTIVES VARIABLES=ZRES DFBETA_1 DFBETA_2 DFBETA_3 DFFIT COOK LEVER.

* Notes:
* - VIF > 5 or TOL < 0.2 may indicate multicollinearity
* - DFBETAs > 1 (in absolute terms) suggest strong influence
* - Cook's Distance > 1 may indicate outliers
* - Leverage > 2*(k+1)/n is high (k=number of predictors)
