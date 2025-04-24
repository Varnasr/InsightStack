* ============================================================
* combine_graphs.do
* Purpose: Combine previously exported graphs into a panel
* Requires: bar_school_type.png, histogram_scores.png
* ============================================================

* NOTE: This file is illustrative. Stata combines live graphs in memory.
* Use this in a .do sequence where graphs are created but not exported yet.

clear all
set more off

import delimited using "education_labels.csv", clear

graph bar (count), over(school_type) name(g1, replace)
histogram test_score, name(g2, replace)

graph combine g1 g2, col(2) title("Bar + Histogram Panel")
graph export "combined_panel_graph.png", replace