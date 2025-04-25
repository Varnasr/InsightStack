
* SPSS Syntax: Cross-tabulation and Chi-square for Employment and Gender.

* Step 1: Load the relevant dataset.
GET FILE='we_employment_survey.sav'.

* Step 2: Crosstab between gender and formal_sector.
* Assuming 'gender' and 'formal_sector' variables exist or are merged from another dataset.
CROSSTABS
  /TABLES=gender BY formal_sector
  /FORMAT=AVALUE TABLES
  /STATISTICS=CHISQ PHI LAMBDA
  /CELLS=COUNT ROW COLUMN TOTAL
  /COUNT ROUND CELL.

* Step 3: Crosstab between education level and employment type.
CROSSTABS
  /TABLES=edu_level_num BY employment_type
  /FORMAT=AVALUE TABLES
  /STATISTICS=CHISQ CONTINGENCY
  /CELLS=COUNT EXPECTED ROW COLUMN TOTAL.
