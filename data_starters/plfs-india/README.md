# PLFS, India

Starter code in Stata, R and Python for the Periodic Labour Force Survey
unit-level data published by MoSPI.

This folder does not contain data and cannot. You register at
[microdata.gov.in](https://microdata.gov.in/) and download your own copy.

## What you are dealing with

PLFS arrives as plain text with no delimiters, no header and no column names,
alongside a layout spreadsheet that gives every field's block, name and byte
position. For January to December 2022 the README shipped with the data
describes exactly two files:

| File | Records | Record length | Contents |
|---|---:|---|---|
| `CHHV1.txt` | 101,934 | 128 + 1 | Household-wise records, visit 1 |
| `CPerV1.txt` | 424,521 | 71 + 1 | Person-wise records, visit 1 |

with the layout in `Data_LayoutPLFS_2022.xlsx`. Nothing in the text file tells
you where a column begins. Everything in this folder is therefore driven by the
layout you downloaded with your data, because byte positions change between
rounds and code that hardcodes them reads the wrong bytes a year later without
complaining.

## The weight is not MLTS divided by 100

MoSPI's README says, verbatim:

> For generating sub-sample wise estimate for the Calendar Year, weight may be
> applied as follows:
>      Final Weight = MLTS/100
>
> For generating combined estimate for the Calendar Year (taking both the
> subsamples together), weights may be applied as follows:
>      Final weight = MLTS/100   if NSS=NSC
>                   = MLTS/200   otherwise.

where, again verbatim:

> NSS (3 bytes) = number of first stage units surveyed within sector x state x
> stratum x substratum for the sub-sample in a Second Stage Stratum for the Panel
>
> NSC (3 bytes) = number of first stage units surveyed within a sector x state x
> stratum x substratum for combined sub-samples in a Second Stage Stratum for
> the Panel
>
> MLTS (10 bytes) = weight or multiplier (in two places of decimal) calculated at
> the level of Second Stage Stratum (SSS) for the Panel

Where `NSS` and `NSC` differ, both interpenetrating sub-samples are present in
that second stage stratum and each record carries half the weight. Dividing
everything by 100 therefore inflates the estimated population wherever they
differ, and does it silently, because ratios are almost unaffected. A labour
force participation rate computed the wrong way looks entirely normal while
every employment level, every count of workers, every total is too large. On the
synthetic fixture here, where half the second stage strata have `NSS` different
from `NSC`, the naive rule inflates the population by a factor of 1.33.

`apply_weight(df, kind="combined")` implements the rule and refuses to run when
`NSS` or `NSC` is absent, rather than falling back to something plausible.

MoSPI adds a caution worth repeating: "Multipliers given in the data file are to
be used for generating annual estimates for the calendar year only."

## Implied decimals

PLFS stores decimals implicitly. `MLTS` is ten bytes holding a number with two
implied decimal places, so `0000123456` means 1234.56. The layout's decimals
column carries this, and the loaders read the divisor from there rather than
from anything written into the code, so a round that changes the convention
still reads correctly.

## The key, and why padding matters

MoSPI gives the common primary key as:

> Quarter =11(2) (i.e., offset 8th byte, length 2 bytes)
> FSU Serial No. = 32(5)
> Hamlet group/sub-block no. = 37(1)
> Second Stage Stratum No. = 38(1)
> Sample Household No. = 39(2)

with the sub-sample code at byte 27. The parenthetical for Quarter does not
agree with the `11(2)` notation used for the rest; take positions from the
layout file, not from prose.

Build the key by zero-padding each part to its declared width. Concatenating the
parts unpadded collapses distinct households onto one key: FSU 1234 with
household 5 and FSU 12345 with household nothing both become `12345`. The merge
then succeeds and is wrong. `build_key` pads from the layout, and
`merge_person_household` refuses to merge when the household key is not unique,
because a merge that multiplies rows inflates every weighted total.

## The design

From MoSPI's note on sample design and estimation procedure:

- **Urban is a rotational panel.** "In this rotational panel scheme each
  selected household in urban areas will be visited four times, one with first
  visit schedule and other three with revisit schedule," giving 75 percent
  matching between consecutive quarters. Panels are 25 percent of the annual
  urban allocation each.
- **Rural has no revisit.** 25 percent of the annual allocation is covered each
  quarter, in interpenetrating sub-samples. "There will not be any revisit in
  the rural samples."
- **Quarterly estimates are urban and CWS.** Annual estimates cover both sectors
  in usual status and CWS.
- **Strata.** Urban strata are formed within each NSS region by town size class
  per Census 2011: stratum 1 is towns under 50,000, stratum 2 is 50,000 to under
  3 lakh, stratum 3 is 3 lakh to under 15 lakh, and strata 4 upward are one per
  city of 15 lakh or more. The rural areas of each NSS region form a rural
  stratum, with a special stratum in rural Nagaland for villages that are
  difficult to access. Rural sub-strata are formed by population.
- **Second stage strata** are formed by the number of household members with
  general education of secondary standard or above: three in rural, four in
  urban. Households are then selected within each by simple random sampling
  without replacement.
- **Size.** 12,800 first stage units annually at the all-India level, being
  7,024 villages and 5,776 UFS blocks.
- **Coverage.** The whole of India except villages in Andaman and Nicobar
  Islands. The 2022 file also excludes Lakshadweep for July to December 2022,
  where fieldwork could not be carried out.

For design-based standard errors the usual approximation is the FSU as the
primary sampling unit and state by sector by stratum by sub-stratum as the
strata, which follows the definition of `NSS` and `NSC` above. Treat it as an
approximation: NSO's published figures come from the estimator set out in its
own note, not from a generic `svyset`.

## Quick start

Stata:

```stata
do load_plfs.do
plfs_load, layout("layout.csv") data("CHHV1.txt") block(household)
plfs_weight, kind(combined)
plfs_key
```

R:

```r
source("load_plfs.R")
layout <- read_layout("layout.csv")
hh <- read_fixed_width("CHHV1.txt", layout, block = "household")
hh <- build_key(apply_weight(hh, "combined"), layout)
```

Python:

```python
from load_plfs import read_layout, read_fixed_width, apply_weight, build_key
layout = read_layout("layout.csv")
hh = build_key(apply_weight(read_fixed_width("CHHV1.txt", layout, block="household")), layout)
```

Or from the shell:

```
python load_plfs.py layout.csv CHHV1.txt --block household --out households.csv
```

## Preparing the layout

The loaders want a CSV with columns `block`, `name`, `start`, `length`,
`decimals` and `label`. Export MoSPI's `Data_Layout` spreadsheet to CSV and
rename its columns to match. Header wording varies between rounds, so several
spellings are accepted for each: `start` also matches "Byte Position",
"Position (From)" and "From"; `length` also matches "Size" and "Bytes";
`decimals` also matches "No. of Decimals" and "Decimal Places".

`read_layout` refuses a layout with overlapping fields, since two columns cannot
occupy one byte and the usual cause is a shifted row that makes every field
after it read the wrong bytes. It also refuses positions below 1, which is what
a layout looks like after someone has helpfully converted it to 0-indexing. Gaps
are reported but allowed, because MoSPI layouts do leave filler bytes.

## Files here

| File | What it is |
|---|---|
| `load_plfs.do` | Stata: `plfs_makedict`, `plfs_load`, `plfs_weight`, `plfs_key`, `plfs_merge` |
| `load_plfs.R` | R equivalents, built on `readr::read_fwf` |
| `load_plfs.py` | Python equivalents, usable as a library or from the shell |
| `make_fixture.py` | Builds a synthetic layout and two fixed-width files for testing |
| `test_load_plfs.py` | 28 checks against those fixtures |
| `test_load_plfs.R` | The same 28 checks in R |

## Testing

No real data is needed. The fixture carries the structure that matters and
nothing else: 1-indexed inclusive positions, implied decimals on the multiplier,
`NSS` and `NSC` that agree in some second stage strata and differ in others, and
a five-part key whose parts need padding. Every value comes from a seeded
generator and none of it is data about anybody.

```
python make_fixture.py --outdir fixtures
python test_load_plfs.py     # 28 checks
Rscript test_load_plfs.R     # the same 28
```

Both suites were run and both pass, and they return identical numbers from the
same fixture: 240 households, 1,099 persons, mean `MLTS` of 1217.72 and a
correct sum of weights of 2190.4 against the naive rule's 2922.5.

Household size is written into one file and the members into another, so the
last check passes only if the byte positions, the zero padding and the merge
are all correct.

Stata has no free runtime, so `load_plfs.do` is the one file here that has not
been executed. The fixture check at the bottom of it takes about a minute and
names the number to look for.

## Sources

- Data file names, record counts, `NSS`, `NSC`, `MLTS`, the weight rule and the
  primary key: *Final Multiplier-posted Unit-Level Data for Schedule 10.4*,
  README accompanying PLFS January-December 2022, Data Processing Division,
  National Sample Survey Office, Kolkata.
- Rotational panel, visits, stratification, sample size and estimation:
  *Note on Sample Design and Estimation Procedure*, MoSPI.
- Both are published at [mospi.gov.in/plfs](https://mospi.gov.in/plfs) and are
  included in the download for each round. Retrieved 2026-09-08.

Where this page and the documents shipped with your round disagree, your round
is right.
