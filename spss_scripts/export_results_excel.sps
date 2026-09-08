
* Export tables to Excel format.
OMS /SELECT TABLES /IF SUBTYPES='Crosstabulation'
  /DESTINATION FORMAT=XLSX OUTFILE='results_summary.xlsx'.
