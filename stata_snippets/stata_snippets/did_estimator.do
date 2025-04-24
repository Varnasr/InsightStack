
* Difference-in-Differences estimation
gen post = year >= 2022
gen treat = district == "Treatment"
gen did = post * treat
reg outcome i.post##i.treat, robust
