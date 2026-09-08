# Data starters

Starter code for real public-use survey microdata, one folder per dataset, in
Stata, R and Python.

The rest of InsightStack teaches technique against data that stands in for
something. `stata_snippets/` imports a `health_survey.csv` and generates age
bands; that is a good way to learn `import delimited` and no help at all to
someone holding an actual survey file. This section is the other half: code that
knows about a specific named dataset, opens the files as they actually arrive,
and handles the things that produce a wrong answer rather than an error.

## What a folder contains

| | |
|---|---|
| `README.md` | Which files to download and from where, what goes wrong silently, and what is not comparable across rounds |
| `load_*.do`, `load_*.R`, `load_*.py` | The same loader in three languages, with the same guards |
| `variables.csv` | Canonical name to the dataset's variable, with scale factors and caveats. Read by the loaders at runtime, so documentation and behaviour cannot drift apart |
| `make_fixture.py` | Builds synthetic files with the structure but no real data, since none of these datasets may be redistributed |
| `test_*.py` | Checks against those fixtures, one per failure mode |

No folder ships data. Every dataset here needs a registration you hold
personally, and the READMEs say which.

## Folders

| Folder | Covers | Languages |
|---|---|---|
| [`dhs-south-asia/`](dhs-south-asia/) | 28 DHS surveys: India (NFHS 1 to 5), Bangladesh, Nepal, Pakistan, Maldives, Afghanistan, Sri Lanka | Stata, R, Python |
| [`plfs-india/`](plfs-india/) | Periodic Labour Force Survey unit-level data: fixed-width text read from the round's own layout | Stata, R, Python |

## Adding one

Copy the shape of `dhs-south-asia/`. A folder earns its place when its loader
opens the real files and its README names at least one error the data makes easy
and quiet. A folder that is a README and a stub is worse than no folder, because
it looks like coverage.

Nothing is listed here before it is built. Under the
[maintenance policy](https://github.com/Varnasr/OpenStacks-for-Change/blob/main/MAINTENANCE.md)
a roadmap entry is a promise to a reader, so datasets appear in the table above
when they work and not before.
