*! load_dhs.do  Starter routines for DHS recode files, South Asia
*! Part of InsightStack / data_starters. MIT licensed.
* ---------------------------------------------------------------------------
* Load a DHS recode file without exhausting memory, set the survey design, and
* stop rather than return a wrong number.
*
* Covers every DHS survey in South Asia (see surveys.csv). One set of routines
* serves India, Bangladesh, Nepal, Pakistan, Maldives, Afghanistan and Sri
* Lanka, because the recode structure is the same in all of them.
*
*   do load_dhs.do
*   dhs_vars, file("IAIR7EFL.DTA") vars(v012 v106 v190 sdist)
*   dhs_load, file("IAIR7EFL.DTA") vars(v012 v106 v190)
*   svy: mean v012
*
* No data ships with this file. Download the recodes yourself from
* dhsprogram.com once your data request is approved; see README.md.
* ---------------------------------------------------------------------------

version 13
capture program drop dhs_recode_of
capture program drop dhs_design_vars
capture program drop dhs_vars
capture program drop dhs_load
capture program drop dhs_anthro
capture program drop dhs_cmc

* ---------------------------------------------------------------------------
* Read the recode type out of a DHS filename.
* DHS names files {CC}{RR}{phase}{release}{format}, so IAIR7EFL.DTA is India,
* Individual Recode, phase 7, release E, flat. Renaming the file breaks this,
* which is why every routine here accepts recode() explicitly.
* ---------------------------------------------------------------------------
program define dhs_recode_of, rclass
    syntax , File(string)
    local f : subinstr local file "\" "/", all
    local stem = substr("`f'", strrpos("`f'", "/") + 1, .)
    local cc = upper(substr("`stem'", 1, 2))
    local rc = upper(substr("`stem'", 3, 2))
    local ph = upper(substr("`stem'", 5, 1))
    if !inlist("`rc'", "IR", "MR", "KR", "BR", "HR", "PR", "CR") {
        display as error "Cannot read a DHS recode type out of '`stem''."
        display as error "Expected something like IAIR7EFL.DTA. If you renamed the"
        display as error "file, pass recode() explicitly."
        exit 198
    }
    return local country "`cc'"
    return local recode  "`rc'"
    return local phase   "`ph'"
end

* ---------------------------------------------------------------------------
* Weight, PSU and strata differ by recode type. Getting this wrong does not
* error; it silently produces standard errors for the wrong design.
* ---------------------------------------------------------------------------
program define dhs_design_vars, rclass
    syntax , Recode(string)
    local rc = upper("`recode'")
    if inlist("`rc'", "IR", "KR", "BR", "CR")      local p ""
    else if "`rc'" == "MR"                          local p "m"
    else if inlist("`rc'", "HR", "PR")              local p "h"
    else {
        display as error "No design defined for recode '`rc''."
        exit 198
    }
    return local weight     "`p'v005"
    return local psu        "`p'v021"
    return local strata     "`p'v022"
    return local strata_alt "`p'v023"
end

* ---------------------------------------------------------------------------
* Report which of the variables you want actually exist in this round, without
* loading a single observation.
*
* This is the cross-round harmonisation problem made visible: v190 is missing
* from pre-2000 rounds, and sdist exists only for India from NFHS-4 onward.
* ---------------------------------------------------------------------------
program define dhs_vars, rclass
    syntax , File(string) [Vars(string)]
    quietly describe using "`file'", varlist
    local present "`r(varlist)'"
    if "`vars'" == "" {
        display as text "`: word count `present'' variables in `file'"
        return local present "`present'"
        exit
    }
    local found ""
    local missing ""
    foreach v of local vars {
        local hit : list v in present
        if `hit' local found "`found' `v'"
        else     local missing "`missing' `v'"
    }
    display as text "  present: `found'"
    if "`missing'" != "" display as result "  not in this file:`missing'"
    return local present "`found'"
    return local missing "`missing'"
end

* ---------------------------------------------------------------------------
* Load selected variables and set the survey design.
*
* vars() is the analysis variables you want. The design variables for the
* recode are added for you, so you never have to remember that the men's recode
* weights on mv005 rather than v005.
* ---------------------------------------------------------------------------
program define dhs_load
    syntax , File(string) [Vars(string) Recode(string) NOSCales NODEsign]

    if "`recode'" == "" {
        dhs_recode_of, file("`file'")
        local recode "`r(recode)'"
        display as text "  `file': recode `recode', phase `r(phase)', country `r(country)'"
    }
    local recode = upper("`recode'")

    dhs_design_vars, recode("`recode'")
    local w    "`r(weight)'"
    local psu  "`r(psu)'"
    local st   "`r(strata)'"
    local stA  "`r(strata_alt)'"

    if "`vars'" != "" {
        * Keep only what exists, otherwise -use- refuses the whole file.
        quietly dhs_vars, file("`file'") vars(`vars' `w' `psu' `st' `stA')
        local keep "`r(present)'"
        local gone "`r(missing)'"
        if "`gone'" != "" display as result "  not in this file:`gone'"
        if "`keep'" == "" {
            display as error "None of the requested variables exist in this file."
            exit 111
        }
        use `keep' using "`file'", clear
    }
    else {
        display as text "  reading every column (slow and memory hungry on large surveys)"
        use "`file'", clear
    }

    * ---- weights -----------------------------------------------------------
    capture confirm variable `w'
    if _rc {
        display as error "`w' is missing, so nothing weighted can be computed from"
        display as error "this file. Include it in your variable list."
        exit 111
    }
    quietly summarize `w'
    if r(N) == 0 {
        display as error "`w' is entirely missing."
        exit 2000
    }
    if r(mean) < 1000 {
        display as error "`w' averages " %12.2fc r(mean) ", far below the ~1,000,000"
        display as error "a raw DHS weight should average. This file looks pre-scaled"
        display as error "or is not a DHS recode. Dividing again would shrink every"
        display as error "weighted total by a million."
        exit 459
    }
    quietly generate double weight = `w' / 1000000
    label variable weight "DHS sample weight (`w' / 1,000,000)"

    * ---- scale factors from variables.csv ---------------------------------
    * Weights are handled above and anthropometry in dhs_anthro, because the
    * 9990-and-above flags have to be spotted before anything divides them down
    * into the plausible range.
    if "`noscales'" == "" {
        foreach pair in "v191 100000" "mv191 100000" "hv271 100000" ///
                        "v437 10" "v438 10" "v456 10" {
            local var : word 1 of `pair'
            local div : word 2 of `pair'
            capture confirm variable `var'
            if !_rc {
                quietly replace `var' = `var' / `div'
                display as text "  scaled `var' by 1/`div'"
            }
        }
    }

    * ---- survey design -----------------------------------------------------
    if "`nodesign'" == "" {
        capture confirm variable `psu'
        if _rc {
            display as result "  `psu' absent; svyset will use observations as clusters"
            local psuvar ""
        }
        else local psuvar "`psu'"

        local stvar ""
        capture confirm variable `st'
        if !_rc local stvar "`st'"
        else {
            capture confirm variable `stA'
            if !_rc {
                local stvar "`stA'"
                display as text "  design strata taken from `stA' (`st' absent, normal in older rounds)"
            }
        }

        * nest is implied: DHS cluster numbers restart within strata.
        if "`stvar'" != "" {
            svyset `psuvar' [pweight=weight], strata(`stvar') singleunit(centered)
        }
        else {
            display as result "  no strata variable found; variance estimates will be"
            display as result "  wrong unless the design really is unstratified"
            svyset `psuvar' [pweight=weight], singleunit(centered)
        }
    }

    display as text "  observations: " %12.0fc `=_N'
    quietly summarize weight
    display as text "  sum of weights: " %12.0fc r(sum) "  (should be close to the observation count)"
end

* ---------------------------------------------------------------------------
* Turn DHS anthropometry into usable z-scores.
*
* Three things go wrong here and none of them raise an error on their own: the
* values are stored times 100, flags and missing sit at 9990 and above, and the
* columns are hw70-hw73 in the children's recode but hc70-hc73 in the household
* member recode. Bounds are the WHO 2006 plausibility limits.
* ---------------------------------------------------------------------------
program define dhs_anthro
    syntax , [Recode(string)]
    local rc = upper("`recode'")
    if "`rc'" == "PR" local p "hc"
    else              local p "hw"

    local names "haz waz whz bmiz"
    local cols  "`p'70 `p'71 `p'72 `p'73"
    local los   "-6 -6 -5 -5"
    local his   "6 5 5 5"

    forvalues i = 1/4 {
        local nm : word `i' of `names'
        local cl : word `i' of `cols'
        local lo : word `i' of `los'
        local hi : word `i' of `his'
        capture confirm variable `cl'
        if _rc continue
        quietly count if `cl' >= 9990 & !missing(`cl')
        local flagged = r(N)
        quietly generate double `nm' = `cl' / 100 if `cl' < 9990 & !missing(`cl')
        quietly count if !missing(`nm') & (`nm' < `lo' | `nm' > `hi')
        local oob = r(N)
        quietly replace `nm' = . if `nm' < `lo' | `nm' > `hi'
        label variable `nm' "`nm' from `cl', WHO 2006 bounds [`lo', `hi']"
        display as text "  `nm' from `cl': `flagged' flagged or missing, `oob' outside WHO bounds"
    }
end

* ---------------------------------------------------------------------------
* Century month code to calendar year and month. CMC 1441 is January 2020.
* ---------------------------------------------------------------------------
program define dhs_cmc
    syntax varname , [Prefix(string)]
    if "`prefix'" == "" local prefix "`varlist'"
    quietly generate int `prefix'_year  = 1900 + floor((`varlist' - 1) / 12)
    quietly generate int `prefix'_month = `varlist' - 12 * (`prefix'_year - 1900)
    label variable `prefix'_year  "Year from `varlist' (CMC)"
    label variable `prefix'_month "Month from `varlist' (CMC)"
end

* ---------------------------------------------------------------------------
* Check the routines against the synthetic fixtures, which carry the structure
* but no data about anybody:
*
*   python make_fixture.py --outdir fixtures
*   do load_dhs.do
*   dhs_load, file("fixtures/XXKR7AFL.DTA") vars(v012 v190 hw70 hw71 b5)
*   dhs_anthro, recode(KR)
*   summarize haz waz
*
* haz should average roughly -1.4 with about 8 percent missing. If it averages
* near zero with nothing missing, the flags were divided instead of dropped.
* ---------------------------------------------------------------------------
