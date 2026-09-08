
* Generate equity plots for coverage
xtile quintile = income, n(5)
collapse (mean) outcome, by(quintile)
twoway (connected outcome quintile), title("Equity Plot")
