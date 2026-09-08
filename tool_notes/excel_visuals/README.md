# Excel

Three chart templates as `.xlsx`, for the colleague who will only ever open
Excel. Each has a data sheet you overwrite and a chart sheet that redraws.

| File | What it makes | Use it for |
|---|---|---|
| `bullet_chart_template.xlsx` | A bar against a target line and shaded bands | Target versus actual, one indicator per row |
| `waterfall_chart_template.xlsx` | Rising and falling bars from a start value to an end value | What moved a total between two periods |
| `gantt_chart_template.xlsx` | Horizontal bars on a date axis | A field schedule, one row per activity |

## When to use it

The audience will edit the numbers themselves, and they work in Excel. A
programme manager updating a bullet chart each quarter needs a file they can
open, not a script they cannot run. These three cover the charts a monitoring
report needs and a default Excel chart does badly.

## When not to

Anything that will be produced more than once from data that arrives as a
file. Pasting into a template is a manual step every time. FieldStack's
`custom_viz/` has the bullet and waterfall charts as R code that reads the
data and draws.

## What goes wrong

Excel charts reference cell ranges. Adding a row below the data does not
extend the chart; the new row is silently left off. Convert the data range to
a Table (Ctrl+T) before pointing the chart at it, and it grows.

Colours are set per series. A chart copied into a report with the
organisation's palette will need each series recoloured; there is no theme
file here, because Excel's chart themes do not travel reliably between
machines.
