* Apply variable and value labels from a data dictionary CSV.
* Stata companion to label_variables/labels.py.
*
* The dictionary has columns variable, label, values, with values written as
* code=label pairs separated by |, e.g. 1=Yes|0=No|-99=Refused. This reads it,
* labels every variable it can find, builds a value label from the values
* column, and tells you which variables in the data have no entry.

local dictionary "label_variables/input/data_dictionary.csv"
local datafile   "your_data.dta"     // set this

preserve
import delimited using "`dictionary'", clear varnames(1) stringcols(_all)
local n = _N
forvalues i = 1/`n' {
    local v`i'   = trim(variable[`i'])
    local lab`i' = trim(label[`i'])
    capture local val`i' = trim(values[`i'])
    if _rc local val`i' ""
}
restore

use "`datafile'", clear

forvalues i = 1/`n' {
    capture confirm variable `v`i''
    if _rc {
        display as error "no variable `v`i'' in the data (in the dictionary)"
        continue
    }
    label variable `v`i'' "`lab`i''"

    if "`val`i''" != "" {
        capture confirm numeric variable `v`i''
        if _rc {
            display as text "`v`i'': value labels only attach to numeric variables; skipped"
            continue
        }
        local pairs : subinstr local val`i' "|" " ", all
        local define ""
        foreach pair of local pairs {
            gettoken code lbl : pair, parse("=")
            local lbl = subinstr("`lbl'", "=", "", 1)
            local define `"`define' `code' "`lbl'""'
        }
        capture label drop `v`i''_lbl
        label define `v`i''_lbl `define'
        label values `v`i'' `v`i''_lbl
    }
}

* Coverage: variables in the data with no dictionary entry.
display as text _n "Unlabelled variables:"
foreach v of varlist _all {
    local l : variable label `v'
    if "`l'" == "" display as result "  `v'"
}
