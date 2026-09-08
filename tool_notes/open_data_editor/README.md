# RawGraphs, Datawrapper and the Open Data Editor

A district indicators CSV shaped for the no-code chart tools, and one chart
made from it so you can see what the shape produces.

| File | What it is |
|---|---|
| `district_health_gaps.csv` | One row per district, one column per indicator: the tidy-wide shape these tools want |
| `stacked_bar_chart.png` | A stacked bar made from it in matplotlib, which is what RawGraphs produces from the same input |

## When to use it

A chart for a report or a slide, made by someone who does not write code, from
data that is already clean. RawGraphs (rawgraphs.io) runs in the browser and
keeps nothing, so it is safe with real data. Datawrapper hosts the chart and
gives you an embed, so it is the right choice when the chart is going on a web
page. The Open Data Editor (from Frictionless Data) is for checking a CSV's
structure before charting it, which is more useful than it sounds.

## When not to

A chart that will be remade when the data updates. All three tools start from
a pasted table and none remembers a pipeline, so the fourth quarterly version
costs the same twenty minutes as the first. And anything that needs a survey
weight: they plot the numbers they are given, and a weighted mean has to be
computed elsewhere first.

## What goes wrong

**Datawrapper hosts your data.** The embed loads from their servers, the data
is on their servers, and a free account's charts are public. District-level
aggregates are usually fine; anything at a finer grain than that, decide first.

**The shape matters more than the tool.** These tools want one row per unit and
one column per series. A "long" file with an `indicator` column and a `value`
column will chart as one stripe. Pivot before pasting.
