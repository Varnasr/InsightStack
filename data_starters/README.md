# Data starters

Loaders for real public-use survey microdata, one folder per dataset, in
Stata, R and Python. Each opens the files as they are distributed and
applies the weight and scale rules that the documentation states.

| Folder | Covers | Languages |
| --- | --- | --- |
| [`dhs-south-asia/`](dhs-south-asia/) | 28 DHS surveys: India (NFHS 1 to 5), Bangladesh, Nepal, Pakistan, Maldives, Afghanistan, Sri Lanka | Stata, R, Python |
| [`plfs-india/`](plfs-india/) | Periodic Labour Force Survey unit-level data, fixed-width text read from the round's own layout | Stata, R, Python |

## What a folder contains

| File | What it is |
| --- | --- |
| `README.md` | Which files to download and from where, what goes wrong silently, what is not comparable across rounds |
| `load_*.do`, `load_*.R`, `load_*.py` | The same loader in three languages |
| `variables.csv` | Canonical name to the dataset's variable, with scale factors and caveats, read at runtime |
| `make_fixture.py` | Builds synthetic files with the structure and no real data |
| `test_*.py`, `test_*.R` | Checks against the fixtures |

No folder ships data. DHS and MoSPI both prohibit redistribution; each README
says what to download.

## Adding a folder

Copy the shape of `dhs-south-asia/`. A folder is listed when its loader opens
the real files and its tests pass, not before.
