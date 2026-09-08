*! load_plfs.do  Starter routines for PLFS unit-level data
*! Part of InsightStack / data_starters. MIT licensed.
* ---------------------------------------------------------------------------
* Read PLFS unit-level data: fixed-width text, driven by the round's own layout.
*
* PLFS arrives from MoSPI's microdata portal as plain text with no delimiters,
* no header and no column names, plus a separate layout spreadsheet giving each
* field's block, name, byte position and length. Nothing in the text file tells
* you where a column starts, so everything here is driven by the layout you
* downloaded with your data. Positions change between rounds, and a do-file that
* hardcodes them quietly reads the wrong bytes a year later.
*
*   do load_plfs.do
*   plfs_load, layout("layout.csv") data("CHHV1.txt") block(household)
*   plfs_weight, kind(combined)
*   plfs_key
*
* The layout must be a CSV with columns: block, name, start, length, decimals.
* Export MoSPI's Data_Layout xlsx to CSV and rename the columns to match; the
* README explains which of MoSPI's headings map to which.
*
* Variable names are lowercased and passed through strtoname(), so
* FSU_Serial_No becomes fsu_serial_no.
*
* No data ships with this file. Register at microdata.gov.in and download the
* round you want; see README.md.
* ---------------------------------------------------------------------------

version 13
capture program drop plfs_makedict
capture program drop plfs_load
capture program drop plfs_weight
capture program drop plfs_key
capture program drop plfs_merge

* ---------------------------------------------------------------------------
* Write an infix dictionary from the layout, and remember each field's width
* and decimal places in global macros for the routines that follow.
*
* MoSPI positions are 1-indexed and inclusive, which is exactly what infix
* expects, so no conversion is needed here. That is not true in every language:
* the Python version has to subtract one.
* ---------------------------------------------------------------------------
program define plfs_makedict, rclass
    syntax , Layout(string) Data(string) [Block(string) Dict(string)]
    if "`dict'" == "" local dict "plfs_dict.dct"

    preserve
    import delimited "`layout'", varnames(1) clear stringcols(_all)
    foreach need in block name start length {
        capture confirm variable `need'
        if _rc {
            display as error "The layout needs a '`need'' column. Rename your MoSPI"
            display as error "layout export's columns to: block name start length decimals"
            restore
            exit 111
        }
    }
    capture confirm variable decimals
    if _rc quietly generate decimals = "0"

    if "`block'" != "" quietly keep if lower(block) == lower("`block'")
    quietly destring start length decimals, replace force
    quietly drop if missing(start) | missing(length)
    quietly sort start
    if _N == 0 {
        display as error "No fields left in the layout for block '`block''."
        restore
        exit 111
    }

    * Overlapping fields mean a shifted row, and every field after it reads the
    * wrong bytes. Refuse rather than produce plausible nonsense.
    quietly generate long endpos = start + length - 1
    quietly generate long prevend = endpos[_n-1]
    quietly count if _n > 1 & start <= prevend
    if r(N) > 0 {
        display as error "`r(N)' overlapping field(s) in the layout. Two columns cannot"
        display as error "occupy one byte; check for a shifted row."
        restore
        exit 459
    }
    quietly count if start < 1
    if r(N) > 0 {
        display as error "Positions must be 1-indexed; `r(N)' field(s) start below 1."
        restore
        exit 459
    }

    local nfields = _N
    local reclen = endpos[`nfields']
    tempname fh
    file open `fh' using "`dict'", write replace text
    file write `fh' `"infix dictionary using "`data'" {"' _n
    forvalues i = 1/`nfields' {
        local nm = strtoname(lower(name[`i']))
        local s  = start[`i']
        local e  = endpos[`i']
        local d  = decimals[`i']
        local w  = length[`i']
        file write `fh' "    double `nm' `s'-`e'" _n
        global PLFS_W_`nm'   = `w'
        global PLFS_DEC_`nm' = `d'
        local names "`names' `nm'"
    }
    file write `fh' "}" _n
    file close `fh'
    restore

    display as text "  dictionary: `nfields' fields, `reclen' bytes -> `dict'"
    return local dict    "`dict'"
    return local names   "`names'"
    return local reclen  "`reclen'"
end

* ---------------------------------------------------------------------------
* Read a PLFS text file and apply the implied decimal places.
*
* PLFS stores decimals implicitly: MLTS is ten bytes holding a number with two
* implied decimal places, so 0000123456 means 1234.56. The scale comes from the
* layout, not from anything written here, so it stays right when a round
* changes it.
* ---------------------------------------------------------------------------
program define plfs_load
    syntax , Layout(string) Data(string) [Block(string) Dict(string) NODECimals]
    plfs_makedict, layout("`layout'") data("`data'") block("`block'") dict("`dict'")
    local dictfile "`r(dict)'"
    local names    "`r(names)'"

    infix using "`dictfile'", clear

    if "`nodecimals'" == "" {
        foreach v of local names {
            local d = "${PLFS_DEC_`v'}"
            if "`d'" != "" & "`d'" != "0" & "`d'" != "." {
                quietly replace `v' = `v' / (10^`d')
                display as text "  `v': `d' implied decimal place(s)"
            }
        }
    }
    display as text "  observations: " %12.0fc `=_N'
end

* ---------------------------------------------------------------------------
* Add the final weight, following MoSPI's rule rather than dividing by 100.
*
* From the README shipped with the data:
*
*     For generating sub-sample wise estimate for the Calendar Year, weight may
*     be applied as follows:
*          Final Weight = MLTS/100
*     For generating combined estimate for the Calendar Year (taking both the
*     subsamples together), weights may be applied as follows:
*          Final weight = MLTS/100   if NSS=NSC
*                       = MLTS/200   otherwise.
*
* NSS is the number of first stage units surveyed in the sub-sample within a
* second stage stratum; NSC is the same count for both sub-samples combined.
* Where they differ, both sub-samples are present and each carries half the
* weight. Dividing everything by 100 doubles the estimated population exactly
* where the sub-samples differ, and does so silently: rates barely move, so a
* participation rate looks fine while every employment total is wrong.
* ---------------------------------------------------------------------------
program define plfs_weight
    syntax , [Kind(string) Weightvar(string)]
    if "`kind'" == "" local kind "combined"
    if "`weightvar'" == "" local weightvar "mlts"
    if !inlist("`kind'", "combined", "subsample") {
        display as error "kind() must be combined or subsample"
        exit 198
    }
    capture confirm variable `weightvar'
    if _rc {
        display as error "`weightvar' is not in the data, so no weighted estimate is"
        display as error "possible. Include it in the fields you read."
        exit 111
    }

    if "`kind'" == "subsample" {
        quietly generate double weight = `weightvar' / 100
        display as text "  sub-sample weight: `weightvar'/100"
    }
    else {
        foreach v in nss nsc {
            capture confirm variable `v'
            if _rc {
                display as error "A combined estimate needs nss and nsc to choose between"
                display as error "`weightvar'/100 and `weightvar'/200, and `v' is missing."
                display as error "Read it in, or use kind(subsample) if that is what you want."
                exit 111
            }
        }
        quietly generate double weight = cond(nss != nsc, `weightvar'/200, `weightvar'/100)
        quietly count if nss != nsc
        local halved = r(N)
        display as text "  combined weight: `weightvar'/100 for " %9.0fc `=_N - `halved'' ///
            " records, `weightvar'/200 for " %9.0fc `halved' " where nss differs from nsc"
    }
    label variable weight "PLFS final weight (MoSPI combined-estimate rule)"
    quietly summarize weight
    display as text "  sum of weights: " %14.0fc r(sum)
end

* ---------------------------------------------------------------------------
* Build the household key, zero-padding each part to its layout width.
*
* MoSPI's common primary key is quarter, FSU serial number, hamlet group or
* sub-block, second stage stratum and sample household number. Concatenating
* them without padding collapses distinct households onto one key: FSU 1234
* with household 5 and FSU 12345 with household nothing both read as "12345".
* The merge then succeeds and is wrong.
*
* Widths come from the globals plfs_makedict set while reading the layout.
* ---------------------------------------------------------------------------
program define plfs_key
    syntax , [Fields(string) Name(string)]
    if "`fields'" == "" ///
        local fields "quarter fsu_serial_no hamlet_group_sub_block_no second_stage_stratum_no sample_household_no"
    if "`name'" == "" local name "hhid"

    local expr ""
    foreach f of local fields {
        capture confirm variable `f'
        if _rc {
            display as error "Key field `f' is not in the data."
            exit 111
        }
        local w = "${PLFS_W_`f'}"
        if "`w'" == "" | "`w'" == "." {
            display as error "No width recorded for `f'. Run plfs_load first so the"
            display as error "layout widths are read."
            exit 198
        }
        local expr `"`expr' + string(`f', "%0`w'.0f")"'
    }
    local expr = substr("`expr'", 3, .)
    quietly generate str `name' = `expr'
    label variable `name' "Household key, zero-padded to the layout widths"

    quietly duplicates report `name'
    display as text "  `name': " %9.0fc `=_N' " records"
end

* ---------------------------------------------------------------------------
* Merge household fields onto person records, refusing a merge that inflates.
*
* A merge on a key that is not unique in the household file multiplies rows and
* inflates every weighted total.
* ---------------------------------------------------------------------------
program define plfs_merge
    syntax , Using(string) [Key(string)]
    if "`key'" == "" local key "hhid"
    local before = _N
    merge m:1 `key' using "`using'", generate(_plfs_merge)
    quietly count if _plfs_merge == 2
    local hh_only = r(N)
    quietly drop if _plfs_merge == 2
    quietly count if _plfs_merge == 1
    local unmatched = r(N)
    if `unmatched' > 0 {
        display as result "  " %9.0fc `unmatched' " person record(s) matched no household"
    }
    if _N != `before' {
        display as error "The merge changed the person row count from `before' to " _N "."
        display as error "The household key is not unique; check the visit or quarter selection."
        exit 459
    }
    display as text "  merged; " %9.0fc `hh_only' " household record(s) had no persons"
end

* ---------------------------------------------------------------------------
* Check these routines against the synthetic fixtures, which carry the structure
* but no data about anybody:
*
*   python make_fixture.py --outdir fixtures
*   do load_plfs.do
*   plfs_load, layout("fixtures/layout.csv") data("fixtures/CHHV1.txt") block(household)
*   plfs_weight, kind(combined)
*
* Expect 240 observations, mean mlts of about 1217.72, and a sum of weights of
* about 2190. If the sum comes out near 2920 the combined rule was not applied
* and every population total is inflated.
* ---------------------------------------------------------------------------
