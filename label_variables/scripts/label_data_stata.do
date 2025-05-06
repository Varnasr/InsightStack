* Apply labels using data_dictionary.csv
import delimited using "../input/data_dictionary.csv", clear
tempfile labels
save `labels'

use your_data_file.dta, clear

foreach var in id age gender income {
    preserve
    use `labels', clear
    keep if variable == "`var'"
    local lbl = label[1]
    restore
    label variable `var' "`lbl'"
}
save your_data_file_labelled.dta, replace