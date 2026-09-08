# Observable

One notebook, its data, and a screenshot.

| File | What it is |
|---|---|
| `district_vulnerability_dashboard.ojs` | Plots vaccine coverage and vaccine availability across districts, with a district selector |
| `public_health_data.csv` | The data it reads |
| `dashboard_screenshot.png` | What it looks like rendered |

Run it by pasting the cells into a notebook at observablehq.com, or with the
Observable CLI (`npm install -g @observablehq/cli`, then `observable preview`)
if you want it local.

## When to use it

An exploratory dashboard that a small team will poke at for a fortnight while
deciding what the real chart should be. Observable is the fastest way to get a
slider attached to a chart, and the reactive model means a change to one cell
updates everything downstream without a rerun.

## When not to

A dashboard anyone outside the team will rely on. Observable notebooks depend
on the platform, an account, and JavaScript loaded from Observable's CDN; a
government partner opening it on a locked-down machine sees nothing. For a
durable dashboard, a static HTML page with the chart library inlined, like
InsightStack's own `calculators/`, works anywhere and needs no account.

## What goes wrong

The CSV is read at runtime by URL, so a notebook that works on your account
breaks when someone forks it and the file attachment does not come along. And
`.ojs` is not JavaScript, whatever the extension suggests: cells are
declarative and execution order is by dependency, so a cell that uses a
variable defined "later" in the file is fine and a loop that mutates one is
not. 
