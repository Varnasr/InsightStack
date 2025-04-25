
* SPSS Syntax: Applying Survey Weights and Stratified Design.

* Assumptions:
* - Data is from a complex survey design.
* - Variables:
*     - weight_var = final analysis weight
*     - psu = primary sampling unit
*     - strata = stratification variable
*     - domain = subpopulation for analysis (optional)

* Step 1: Load dataset.
GET FILE='we_employment_survey.sav'.

* Step 2: Declare the complex sampling plan.
COMPLEX SAMPLES PLAN FILE='we_survey_plan.csaplan'.

* Note: The plan file must be created via SPSS Complex Samples > Prepare Plan File wizard,
* or manually using CSPLAN syntax as below:

* Manual method (alternative to GUI):
CSPLAN ANALYSIS
  /PLAN FILE='we_survey_plan.csaplan'
  /PLANVARS ANALYSISWEIGHT=weight_var
            STRATUM=strata
            CLUSTER=psu.

* Step 3: Use weight in a descriptive analysis.
CSDESCRIPTIVES
  /PLAN FILE='we_survey_plan.csaplan'
  /SUMMARY VARIABLES=wages weekly_hours
  /MEAN STDERR.

* Step 4: Use weight in a cross-tabulation.
CSTABULATE
  /PLAN FILE='we_survey_plan.csaplan'
  /TABLES=education_level BY employment_type
  /CELLS=COUNT COLUMNPCT
  /STATISTICS=CHISQ.

* Notes:
* - Always declare the plan first using CSPLAN or GUI wizard.
* - Using the weight variable directly (without plan) gives incorrect SEs.
* - Weight = inverse of selection probability, adjusted for non-response and post-stratification.
* - Clustering and stratification must match the survey's design.

* Output:
* - Design-adjusted SEs, weighted means, and p-values for stratified samples.
