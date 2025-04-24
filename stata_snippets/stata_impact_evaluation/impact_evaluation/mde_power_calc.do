* ============================================================
* mde_power_calc.do
* Purpose: Calculate minimum detectable effect for a t-test
* ============================================================

clear all
set more off

* Example power calc for two-group comparison
power twomeans 5000 5200, sd(1000) alpha(0.05) power(0.8)