
* SPSS Syntax: Missing Data Checks and Diagnostics.

* Step 1: Load the dataset.
GET FILE='we_employment_survey.sav'.

* Step 2: Frequency-based missing value checks.
FREQUENCIES VARIABLES=age wages weekly_hours edu_level_num
  /MISSING=INCLUDE
  /FORMAT=NOTABLE
  /STATISTICS=MINIMUM MAXIMUM.

* Step 3: Visual missing data pattern.
MISSING VALUES age wages weekly_hours edu_level_num (-9999).

* Step 4: Use MVA (Missing Value Analysis) procedure.
MVA
  VARIABLES=age wages weekly_hours edu_level_num
  /MISSING=LISTWISE
  /DESCRIPTIVES=MEAN STDDEV N VALID MISSING
  /COVARIANCE=CORRELATION
  /PLOT=PATTERN.

* Step 5: Set missing value codes (if needed).
* RECODE age wages weekly_hours edu_level_num (-9999=SYSMIS).

* Notes:
* - Replace -9999 with actual user-defined missing codes if used.
* - MVA gives correlation matrix, pattern plots, and missing %.
