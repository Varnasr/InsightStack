# DHS recode files, South Asia

Starter code in Stata, R and Python for the Demographic and Health Surveys of
India, Bangladesh, Nepal, Pakistan, Maldives, Afghanistan and Sri Lanka. Twenty-eight surveys, one loader: the recode structure is the same in all of
them.

This folder does not contain data and cannot. The DHS Program licence lets you
use the files, not pass them on, so everyone downloads their own copy. 

## What the loaders do

They read only the columns you name from a recode such as `IAIR7EFL.DTA`
(724,115 women, about five thousand variables), attach the weight and design
variables for that recode, apply the documented scale factors, and stop with an
explanation when something is off.

## Getting the files

1. Register at [dhsprogram.com](https://dhsprogram.com/data/), describe your
   project, and request access. Access is granted per country, so India and
   Bangladesh are two separate requests.
2. Download the recode you need in Stata (`.DTA`) or SPSS (`.SAV`) format. The
   flat `.DAT` files need the accompanying dictionary and are more work for no
   gain here.
3. Keep the file under its DHS name. The name carries the country, recode type
   and version, and these scripts read all three from it.

`IAIR7EFL.DTA` is India, Individual Recode, phase 7, version E, flat. The version
character changes when DHS reissues a file, and it can be a digit: NFHS-4's
individual recode is `IAIR74FL.DTA`. If you rename the file, pass the recode type
explicitly instead.

## Which file you want

| Recode | Contents | One row is | Weight |
|---|---|---|---|
| `IR` | Individual, women 15-49 | a woman | `v005` |
| `MR` | Men | a man | `mv005` |
| `KR` | Births in the last 5 years | a child, living or dead | `v005` |
| `BR` | Births, full history | a birth, living or dead | `v005` |
| `HR` | Households | a household | `hv005` |
| `PR` | Household members | a person, any age | `hv005` |
| `CR` | Couples | a matched couple | `v005` |

`KR` covers the last five years and `BR` the woman's complete birth history, so
under-five mortality rates come from `BR`. Both include children who have died,
which is why anthropometry work on `KR` has to filter on `b5 == 1` first. Child
anthropometry appears in both `KR` and `PR`, under different variable names.

## Quick start

Stata:

```stata
do load_dhs.do
dhs_vars, file("IAIR7EFL.DTA") vars(v012 v106 v190 sdist)   // what exists here?
dhs_load, file("IAIR7EFL.DTA") vars(v012 v106 v190)
svy: mean v012
```

R:

```r
source("load_dhs.R")
ir  <- read_recode("IAIR7EFL.DTA", c("v012", "v106", "v190"))
des <- dhs_design(ir)
survey::svymean(~v012, des)
```

Python:

```python
from load_dhs import read_recode, clean_anthropometry
ir = read_recode("IAIR7EFL.DTA", ["v012", "v106", "v190"])
kr = clean_anthropometry(read_recode("IAKR7EFL.DTA", ["hw70", "b5", "v190"]), "KR")
```

Or from the shell:

```
python load_dhs.py IAKR7EFL.DTA --vars v190 hw70 hw71 b5 --anthro --out stunting.csv
```

## What goes wrong silently

Each of these produces a plausible number rather than an error.

**Weights are stored with six implied decimals.** `v005` averages about a million
and has to be divided by 1,000,000. Leaving it out does not change a weighted
mean, because the scale cancels, so the error survives every sanity check you are
likely to run. It multiplies every weighted count and total by a million. The
loaders divide it and refuse to run on a file whose weights average under 1,000,
which is what an already-divided file looks like.

**The design variables change with the recode.** The men's recode weights on
`mv005` and clusters on `mv021`. Analysing men with `v005` does not fail; those
variables simply are not there, and if you have merged files they may be there and
wrong. Use `v021` for the PSU rather than `v001`, and `v022` for strata, falling
back to `v023` in older rounds.

**Anthropometry is stored times 100, with flags above it.** `hw70` of `-162` means
a height-for-age z-score of -1.62. Values of 9996 and up are flags and missing.
Divide before you drop them and every flagged child becomes a plausible 99.96,
then a plausible 0.9996, and your stunting rate falls.

**The anthropometry columns are named differently in different recodes.** `hw70`
to `hw73` in the children's recode, `hc70` to `hc73` in the household member
recode. Ask for the wrong pair and you get nothing rather than an error.

**Dead children stay in the birth history.** `BR` and `KR` include children who
have died. Filter on `b5 == 1` for analyses of living children, and do not filter
on it for mortality.

**Region codes are not comparable across rounds.** `v024` in NFHS-3 (2005-06),
NFHS-4 (2015-16) and NFHS-5 (2019-21) uses three different state code sets:
Telangana was created in 2014 and Ladakh separated from Jammu and Kashmir in 2019.
Nothing in the file tells you this. Map to names round by round before pooling.

**Wealth quintiles are relative to their own survey.** `v190` is constructed
within each survey, so quintile 1 in Bangladesh 2022 and quintile 1 in India
2019-21 are not the same standard of living, and neither are quintile 1 in NFHS-4
and NFHS-5. Use `v191`, the underlying score, if you need something continuous,
and remember that it is still survey-specific.

**Century month codes.** `v008` and `b3` are months since January 1900, so
January 2020 is 1441. `cmc_to_year_month` in each script converts them.

## Checking your answer

`benchmarks/nfhs5_stunting.csv` holds the figures DHS published for India's
NFHS-5 child stunting: 35.5 percent nationally, 46.1 in the poorest wealth
quintile falling to 22.9 in the richest, with breakdowns by residence and
mother's education. NFHS-4's national figure of 38.4 is there for comparison.

Two worked examples reproduce the table, one in R and one in Python:

- [FieldStack](https://github.com/Varnasr/FieldStack) `survey_tools/dhs_stunting.R`
- [EquityStack](https://github.com/Varnasr/EquityStack) `survey_estimation/dhs_stunting.py`

Both consume the CSV this loader writes, so the repositories are coupled through
a file rather than a dependency.

## Across rounds

`variables.csv` maps a canonical name to the variable in each recode, with its
scale factor and the caveats that apply. The loaders read the scale factors from
that file at runtime, so the documented scale and the applied scale cannot drift
apart.

Before pooling rounds, run the variable check first. It tells you what is missing
from the older file rather than letting a merge fill it with nothing:

```stata
dhs_vars, file("IAIR52FL.DTA") vars(v190 v191 sdist)
```

`v190` is absent from rounds before roughly 2000. `sdist` exists for India from
NFHS-4 onward only, which is why NFHS-5 supports district estimates and NFHS-3
does not.

## The surveys

Pulled from the DHS Program API on 2026-09-08. Sample sizes are the counts DHS
publishes for the survey, not the row count of any particular recode file.

| Survey | Country | Round | Fieldwork | Released | Women 15-49 | Men |
|---|---|---|---|---|---:|---:|
| `IA1993DHS` | India | 1992-93 | 1992-04 to 1993-09 | 1995-08-01 | 89,777 | not collected |
| `IA1999DHS` | India | 1998-99 | 1998-11 to 1999-12 | 2000-10-01 | 90,303 | not collected |
| `IA2006DHS` | India | 2005-06 | 2005-11 to 2006-08 | 2007-09-01 | 124,385 | 74,369 |
| `IA2015DHS` | India | 2015-16 | 2015-01 to 2016-12 | 2018-01-11 | 699,686 | 112,122 |
| `IA2020DHS` | India | 2019-21 | 2019-06 to 2021-04 | 2022-03-03 | 724,115 | 101,839 |
| `PK1991DHS` | Pakistan | 1990-91 | 1990-12 to 1991-05 | 1992-07-01 | 6,611 | 1,354 |
| `PK2006DHS` | Pakistan | 2006-07 | 2006-09 to 2007-02 | 2008-07-18 | 10,023 | not collected |
| `PK2012DHS` | Pakistan | 2012-13 | 2012-10 to 2013-04 | 2014-01-22 | 13,558 | 3,134 |
| `PK2017DHS` | Pakistan | 2017-18 | 2017-11 to 2018-04 | 2019-02-25 | 15,068 | 3,691 |
| `BD1994DHS` | Bangladesh | 1993-94 | 1993-11 to 1994-03 | 1994-12-01 | 9,640 | 3,284 |
| `BD1997DHS` | Bangladesh | 1996-97 | 1996-11 to 1997-03 | 1997-12-01 | 9,127 | 3,346 |
| `BD2000DHS` | Bangladesh | 1999-00 | 1999-11 to 2000-03 | 2001-05-01 | 10,544 | 2,556 |
| `BD2004DHS` | Bangladesh | 2004 | 2004-01 to 2004-05 | 2005-05-01 | 11,440 | 4,297 |
| `BD2007DHS` | Bangladesh | 2007 | 2007-03 to 2007-08 | 2009-03-24 | 10,996 | 3,771 |
| `BD2011DHS` | Bangladesh | 2011 | 2011-07 to 2011-12 | 2013-02-04 | 17,842 | 3,997 |
| `BD2014DHS` | Bangladesh | 2014 | 2014-06 to 2014-11 | 2016-03-23 | 17,863 | not collected |
| `BD2017DHS` | Bangladesh | 2017-18 | 2017-10 to 2018-03 | 2020-12-14 | 20,127 | not collected |
| `BD2022DHS` | Bangladesh | 2022 | 2022-08 to 2022-12 | 2024-09-09 | 30,078 | not collected |
| `NP1996DHS` | Nepal | 1996 | 1996-01 to 1996-06 | 1997-03-01 | 8,429 | not collected |
| `NP2001DHS` | Nepal | 2001 | 2001-01 to 2001-06 | 2002-04-01 | 8,726 | 2,261 |
| `NP2006DHS` | Nepal | 2006 | 2006-02 to 2006-08 | 2007-05-01 | 10,793 | 4,397 |
| `NP2011DHS` | Nepal | 2011 | 2011-01 to 2011-06 | 2012-03-27 | 12,674 | 4,121 |
| `NP2016DHS` | Nepal | 2016 | 2016-06 to 2017-01 | 2017-11-13 | 12,862 | 4,063 |
| `NP2022DHS` | Nepal | 2022 | 2022-01 to 2022-06 | 2023-06-23 | 14,845 | 4,913 |
| `LK1987DHS` | Sri Lanka | 1987 | 1987-01 to 1987-03 | 1988-05-01 | 5,865 | not collected |
| `MV2009DHS` | Maldives | 2009 | 2009-01 to 2009-10 | 2010-11-23 | 7,131 | 1,727 |
| `MV2016DHS` | Maldives | 2016-17 | 2016-03 to 2017-11 | 2019-02-25 | 7,699 | 4,342 |
| `AF2015DHS` | Afghanistan | 2015 | 2015-06 to 2016-02 | 2017-02-15 | 29,461 | 10,760 |

Sri Lanka appears once. The 1987 survey is the only Sri Lankan round distributed
as DHS recode files; the later Demographic and Health Surveys of 2006-07 and
2016 were run by the Department of Census and Statistics and are obtained from
them directly, in a different format. Afghanistan has a single round, 2015.

## Files here

| File | What it is |
|---|---|
| `load_dhs.do` | Stata routines: `dhs_vars`, `dhs_load`, `dhs_anthro`, `dhs_cmc` |
| `load_dhs.R` | R equivalents, plus `dhs_design()` for the survey package |
| `load_dhs.py` | Python equivalents, usable as a library or from the shell |
| `variables.csv` | Canonical name to recode variable, with scale factors and caveats |
| `surveys.csv` | The 28 South Asia surveys, from the DHS API |
| `make_fixture.py` | Builds synthetic DHS-shaped files for testing |
| `test_load_dhs.py` | 30 checks against those fixtures |
| `test_load_dhs.R` | The same 33 checks in R, plus the survey design object |
| `benchmarks/` | Figures DHS published, to check your pipeline against |

## Testing

No real data is needed. `make_fixture.py` writes small synthetic files carrying
the structure that matters, raw weights near a million, anthropometry times 100
with flags at 9990 and above, century month codes, the `mv` prefix in the men's
recode. Every value comes from a seeded generator and none of it is data about
anybody.

```
python make_fixture.py --outdir fixtures
python test_load_dhs.py     # 30 checks
Rscript test_load_dhs.R     # 33: the same ones, plus the design object
```

The R suite mirrors the Python one and adds three checks for the survey
design object. Verified on Python 3 with pandas and pyreadstat, and on R 4.3.3
with survey 4.2.1 and haven 2.5.4; both return the same numbers from the same
fixture.

Stata has no free runtime, so `load_dhs.do` is the one file here that has not been
executed. It carries the same logic and the same guards, and the fixture check at
the bottom of it takes about a minute. Run that once before trusting it on real
data.

## Sources

- Survey list, fieldwork dates, release dates and sample sizes: DHS Program API,
  `api.dhsprogram.com/rest/dhs/surveys`, retrieved 2026-09-08.
- Recode structure, variable naming and scale factors: *Guide to DHS Statistics*
  and the recode manual for each phase, published at
  [dhsprogram.com/publications](https://dhsprogram.com/publications/).
- Anthropometry plausibility bounds: WHO Child Growth Standards, 2006.

Where this folder and your survey's codebook disagree, the codebook is right.
