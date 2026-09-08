
* SPSS Syntax: Reshape Data from Wide to Long Format.

* Assumption:
* - Dataset has repeated measures like wage_2019, wage_2020, wage_2021 for each respondent.
* - We'll simulate reshaping from wide to long.

* Step 1: Load the dataset (create a dummy if needed).
GET FILE='we_employment_survey.sav'.

* Step 2: Use VARSTOCASES to reshape.
VARSTOCASES
  /MAKE wage FROM wage_2019 wage_2020 wage_2021
  /INDEX=year(2020, 2021, 2022)
  /KEEP=respondent_id age education_level
  /NULL=DROP.

* After reshaping:
* - Each row is now a year-observation for each respondent.
* - The variable 'year' indexes which wage it was.

* Note:
* - This only works if your dataset has wide-format repeated measures.
* - Use CASESTOVARS to reverse the process (long → wide).
