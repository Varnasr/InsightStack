* ============================================================
* propensity_score_matching.do
* Purpose: Estimate treatment effects using propensity score matching
* Input: impact_eval_data.csv
* ============================================================

clear all
set more off

import delimited using "impact_eval_data.csv", clear

teffects psmatch (outcome) (treated age income), atet