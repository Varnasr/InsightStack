
* SPSS Syntax: Macro and Loop Demonstration.

* Purpose:
* - Automate summary statistics for multiple variables
* - Reduce repetition in long scripts
* - Helpful in surveys with 20+ items in the same scale or type

* Step 1: Define the macro.
DEFINE !summarize (varlist=!CMDEND)
  FREQUENCIES VARIABLES=!varlist
  /STATISTICS=MODE MEDIAN
  /ORDER=ANALYSIS.
!ENDDEFINE.

* Step 2: Call the macro with a list of variables.
!summarize age weekly_hours wages edu_level_num.

* Step 3: Loop through variables to compute means by employment type.
DO REPEAT var=age weekly_hours wages.
  MEANS TABLES=var BY employment_type
    /CELLS=MEAN COUNT STDDEV.
END REPEAT.

* Notes:
* - Macros work like reusable functions
* - DO REPEAT is a basic loop (no conditional logic)
* - For advanced loops or data simulation, use Python integration in SPSS
