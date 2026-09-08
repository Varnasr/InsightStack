# Power BI

An adaptation note. No `.pbix` file ships here, and none is going to: a Power BI
report is bound to its data source, and a template with no data behind it is a
blank canvas with a menu.

| File | What it is |
|---|---|
| `mel_dashboard_screenshot.png` | What a MEL dashboard in Power BI looks like, for reference |

Start from Microsoft's own Human Resources sample (`.pbix`, linked from
learn.microsoft.com under "sample datasets"), which opens in Power BI Desktop
and has a layout worth repurposing.

## When to use it

A dashboard for an organisation that already runs on Microsoft 365. If the
team's data is in SharePoint and Excel and the licences are already paid for,
Power BI is the path of least resistance and the IT department will support it.
It handles disaggregation well: slicers on gender, district and age group, and
drillthrough from a summary to the block.

## When not to

A dashboard for anyone *outside* that organisation. Sharing a Power BI report
externally needs a Pro licence on the viewing side too, and a government
partner or a community organisation generally does not have one. For an
external audience, a static HTML page (see InsightStack's `calculators/`) or a
PDF export works without asking anyone to buy anything.

## What goes wrong

**The refresh schedule is the product.** A dashboard is only as current as its
last refresh, and a `.pbix` on someone's laptop refreshes when they open it.
Publishing to the service with a scheduled refresh against a source the
organisation controls is the whole setup; without it you have a screenshot
with slicers.

**Unicode.** Power BI renders Indic scripts, but the default fonts do not
include them all, so a Hindi label renders as boxes until the font is changed
in the visual. Check on the machine the audience will use, not on yours.
