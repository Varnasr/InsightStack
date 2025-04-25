
* SPSS Syntax: Stratified Analysis Example.

* Step 1: Load the dataset.
GET FILE='education_outcomes_by_gender.sav'.

* Step 2: Crosstab: Grade Achieved by Caste, Stratified by Gender.
SORT CASES BY gender.
SPLIT FILE BY gender.

CROSSTABS
  /TABLES=caste BY grade_achieved
  /FORMAT=AVALUE TABLES
  /STATISTICS=CHISQ
  /CELLS=COUNT ROW COLUMN TOTAL.

* Step 3: Reset split file.
SPLIT FILE OFF.

* Notes:
* - This stratifies analysis by gender to explore caste-based performance differences.
* - Replace grade_achieved with any continuous or ordinal variable for subgroup analysis.
