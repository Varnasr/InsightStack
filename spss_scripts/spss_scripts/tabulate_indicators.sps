
* Crosstab analysis by gender and district.
CROSSTABS /TABLES=indicator BY gender_recoded BY district
  /CELLS=COUNT ROW COLUMN TOTAL
  /FORMAT=AVALUE TABLES.
