
* SPSS Syntax: Data Cleaning and Recoding for WEE Employment Dataset.

* Step 1: Load data (to be replaced with actual SAV file location).
GET FILE='we_employment_survey.sav'.

* Step 2: Variable listing and structure.
DISPLAY DICTIONARY.

* Step 3: Check for missing values.
FREQUENCIES VARIABLES=age education_level employment_type weekly_hours wages
  /MISSING=INCLUDE.

* Step 4: Define missing values (if any income or hours < 0 or > 100).
IF (weekly_hours < 0 OR weekly_hours > 100) weekly_hours = $SYSMIS.
IF (wages < 0 OR wages > 20000) wages = $SYSMIS.

* Step 5: Recode education into ordinal scale.
RECODE education_level
  ('Primary' = 1) 
  ('Secondary' = 2) 
  ('Higher Secondary' = 3) 
  ('Graduate' = 4) 
  INTO edu_level_num.
VARIABLE LABELS edu_level_num 'Education Level (Ordinal)'.
VALUE LABELS edu_level_num 1 'Primary' 2 'Secondary' 3 'Higher Secondary' 4 'Graduate'.

* Step 6: Bin age into groups.
DO IF (age >= 18 AND age <= 25).
  COMPUTE age_group = 1.
ELSE IF (age > 25 AND age <= 35).
  COMPUTE age_group = 2.
ELSE IF (age > 35).
  COMPUTE age_group = 3.
END IF.
VARIABLE LABELS age_group 'Age Group'.
VALUE LABELS age_group 1 '18–25' 2 '26–35' 3 '36+'.

* Step 7: Collapse employment types: Regular & Self-employed = 'Formal', Casual = 'Informal'.
RECODE employment_type
  ('Self-employed' 'Regular' = 1)
  ('Casual' = 0)
  INTO formal_sector.
VARIABLE LABELS formal_sector 'Employment in Formal Sector (1=Yes, 0=No)'.
VALUE LABELS formal_sector 1 'Formal' 0 'Informal'.

* Step 8: Post-cleaning frequencies.
FREQUENCIES VARIABLES=edu_level_num age_group formal_sector.
