# InsightStack

MEL tools, calculators, research documentation, and loaders for real survey
microdata. Part of the [OpenStacks](https://openstacks.dev) family. Status:
Stable, per the family [maintenance policy](https://github.com/Varnasr/OpenStacks-for-Change/blob/main/MAINTENANCE.md).

## Layout

Polyglot by design: Stata, Python, R, SPSS. See the README table for the full
list. Two parts matter most when working here.

- `stata_snippets/`, `spss_scripts/`, `label_variables/`, `data_validation/` —
  technique taught against stand-in data. `import_cleaning.do` reads a
  `health_survey.csv` that does not exist. That is deliberate and fine.
- `data_starters/` — the opposite: code that knows a specific named dataset and
  opens the files as they actually arrive. One folder per dataset, each with the
  same loader in Stata, R and Python, a README naming the raw files to fetch, and
  tests against seeded synthetic fixtures.

## data_starters conventions

- **No data ships and none can.** DHS and MoSPI both prohibit redistribution.
  Every folder has a `make_fixture.py` that builds synthetic files carrying the
  structure and nobody's data. `fixtures/` is gitignored.
- **Scale factors and byte positions are read at runtime**, from `variables.csv`
  for DHS and from the round's own layout for PLFS, never hardcoded. Documented
  behaviour and applied behaviour cannot then drift apart.
- **A folder earns its place** when its loader opens the real files and its
  README names at least one error the data makes easy and quiet. A folder that
  is a README and a stub is worse than none, because it looks like coverage.
- **Nothing is listed before it is built.** Maintenance policy rule 1: a roadmap
  entry is a promise to a reader.

## Testing

`.github/workflows/tests.yml` runs everything on pull requests and pushes to
main. No schedule: nothing here touches an external service, so nothing rots
between commits.

```
cd data_starters/dhs-south-asia && python make_fixture.py --outdir fixtures
python test_load_dhs.py     # 30 checks
Rscript test_load_dhs.R     # 33: the same ones plus the survey design object

cd ../plfs-india && python make_fixture.py --outdir fixtures
python test_load_plfs.py    # 28 checks
Rscript test_load_plfs.R    # the same 28
```

Stata has no free runtime, so the `.do` files are the only untested ones. Each
carries a fixture check at the bottom naming the number to look for. Say so
plainly rather than implying otherwise.

## Watch out for

- **DHS weights** are `v005 / 1,000,000`, and the men's recode weights on
  `mv005`. Omitting the division leaves means intact and multiplies every
  weighted total by a million, so it survives casual checking.
- **DHS anthropometry** flags sit at 9990 and above and must be dropped *before*
  the values are divided by 100, not after. Getting this backwards turns flagged
  children into plausible z-scores and lowers your stunting rate.
- **PLFS weights** are not `MLTS/100`. For a combined estimate it is `MLTS/100`
  only where `NSS = NSC`, and `MLTS/200` otherwise. The blanket rule inflates the
  population wherever the sub-samples differ, silently, because ratios barely
  move.
- **Published tables are the check.** `data_starters/dhs-south-asia/benchmarks/`
  holds the figures DHS published. Reproducing them is the only cheap proof a
  pipeline is right end to end.

## Related repositories

The analysis half of the chain lives elsewhere, coupled through a CSV rather
than a dependency: [EquityStack](https://github.com/Varnasr/EquityStack)
`survey_estimation/` in Python, [FieldStack](https://github.com/Varnasr/FieldStack)
`survey_tools/dhs_stunting.R` in R.

## Design references

For any UI or design refresh work on this repository or elsewhere in the family,
draw from **[kombai.com/gallery/web](https://kombai.com/gallery/web)** — the
owner's preferred reference for interface work that is genuinely well made. This
applies across all of Varna's repositories and sites, not only this one.

What actually has an interface, counted rather than assumed:

| Repository | HTML | Published |
|---|---|---|
| InsightStack | 8 files: six interactive calculators in `calculators/`, a Taguette coding page, a root `index.html` | GitHub Pages, Jekyll `minima` theme via `_config.yml` |
| FieldStack | one root `index.html` | GitHub Pages |
| EquityStack | none | not published |

The six calculators are the largest design surface in the stack family and the
obvious place to start. Beyond the stacks: SignalStack, Experiments,
openstacks.dev and the ImpactMojo properties.

One constraint that catches people: `Experiments` serves under a strict Content
Security Policy allowlisting specific CDNs, so a design pulling fonts or scripts
from anywhere else fails there silently. Read its `netlify.toml` before adding
any external asset.
