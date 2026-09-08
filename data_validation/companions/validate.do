* Validate a dataset against a data dictionary: duplicates, required, ranges,
* allowed values. Stata companion to data_validation/validate.py, which is the
* reference and does more (types, name style, column set, cross-file ids).
*
* Usage, from the repository root:
*   do data_validation/companions/validate.do
* after setting the two locals below.

local dictionary "data_validation/sample_data/data_dictionary.csv"
local datafile   "data_validation/sample_data/sample_data.csv"
local idvar      "id"

* Sentinel codes that mean missing, so a range check does not report them.
local sentinels  -999 -998 -99 -88 -9

* --- read the dictionary into locals ------------------------------------------
preserve
import delimited using "`dictionary'", clear varnames(1) stringcols(_all)
local n = _N
forvalues i = 1/`n' {
    local v`i'   = variable[`i']
    local req`i' = lower(trim(required[`i']))
    local min`i' = trim(min[`i'])
    local max`i' = trim(max[`i'])
    local all`i' = trim(allowed[`i'])
}
restore

import delimited using "`datafile'", clear varnames(1)

* --- identifier ---------------------------------------------------------------
display as text _n "== identifier"
capture confirm string variable `idvar'
if _rc == 0 {
    count if missing(`idvar') | trim(`idvar') == ""
}
else {
    count if missing(`idvar')
}
display as result "  blank ids: " r(N)
duplicates report `idvar'
duplicates tag `idvar', gen(_dup)
list `idvar' if _dup > 0, noobs
drop _dup

* --- per variable -------------------------------------------------------------
forvalues i = 1/`n' {
    local v "`v`i''"
    capture confirm variable `v'
    if _rc {
        display as error "  `v': listed in the dictionary but absent from the file"
        continue
    }
    capture confirm numeric variable `v'
    local isnum = (_rc == 0)

    * treat sentinels as missing for the numeric checks
    if `isnum' {
        tempvar clean
        gen double `clean' = `v'
        foreach s of local sentinels {
            replace `clean' = . if `clean' == `s'
        }
    }

    if inlist("`req`i''", "yes", "y", "true", "1") {
        if `isnum' count if missing(`clean')
        else       count if missing(`v') | trim(`v') == ""
        if r(N) > 0 {
            display as error "  `v': required but blank in " r(N) " row(s)"
            if `isnum' list `idvar' if missing(`clean'), noobs
            else       list `idvar' if missing(`v') | trim(`v') == "", noobs
        }
    }

    if `isnum' & ("`min`i''" != "" | "`max`i''" != "") {
        local cond ""
        if "`min`i''" != "" local cond "`clean' < `min`i''"
        if "`max`i''" != "" {
            if "`cond'" != "" local cond "`cond' | "
            local cond "`cond'`clean' > `max`i''"
        }
        count if (`cond') & !missing(`clean')
        if r(N) > 0 {
            display as error "  `v': " r(N) " value(s) outside [`min`i'', `max`i'']"
            list `idvar' `v' if (`cond') & !missing(`clean'), noobs
        }
    }

    if "`all`i''" != "" {
        local opts : subinstr local all`i' "|" `"" ""'", all
        if `isnum' {
            count if !inlist(string(`v'), "`opts'") & !missing(`clean')
            if r(N) > 0 {
                display as error "  `v': " r(N) " value(s) not in {`all`i''}"
                list `idvar' `v' if !inlist(string(`v'), "`opts'") & !missing(`clean'), noobs
            }
        }
        else {
            count if !inlist(trim(`v'), "`opts'") & trim(`v') != ""
            if r(N) > 0 {
                display as error "  `v': " r(N) " value(s) not in {`all`i''}"
                list `idvar' `v' if !inlist(trim(`v'), "`opts'") & trim(`v') != "", noobs
            }
        }
    }
    capture drop `clean'
}
display as text _n "done. Nothing above was changed; fix in the source, not here."
