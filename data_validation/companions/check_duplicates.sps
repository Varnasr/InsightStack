* SPSS syntax to check for duplicate cases by respondent_id;
SORT CASES BY respondent_id.
MATCH FILES /FILE=* /BY respondent_id /FIRST=Primary.
SELECT IF NOT Primary.
FREQUENCIES VARIABLES=respondent_id.