# data_validation

A list of what is wrong with a file, by identifier, before it reaches a finding.

```python
from data_validation import validate, Rules

rules = Rules.from_csv("sample_data/data_dictionary.csv", id="id", names="snake_case")
report = validate(df, rules)
report.issues        # one row per problem: id, variable, value, check, message
report.summary()     # counts by check and severity
report.ok            # True only when nothing fired
```

```
python data_validation/test_data_validation.py    # 18 tests, 40 checks
```

## What it checks

| Check | Fires when |
|---|---|
| `id_blank`, `id_duplicate` | The identifier is missing or repeated |
| `required_blank` | A variable listed as required is blank, NA, `.`, or a sentinel code |
| `out_of_range` | A numeric value falls outside a declared `(min, max)`; either end may be open |
| `not_allowed` | A value is not in the declared list, compared as trimmed strings |
| `type_numeric`, `type_integer`, `type_binary`, `type_date` | A value cannot be read as the declared type, reported per value |
| `name_style` | A column name breaks `snake_case` or Stata's 32-character rule |
| `column_missing`, `column_unexpected` | The file's columns differ from the dictionary's |
| `orphan_child`, `childless_parent` | `check_cross_file_ids`: a roster row whose household is not in the household file, and the reverse |

## Rules come from the dictionary

`Rules.from_csv` reads the same dictionary that `label_variables/` uses. Add
`type`, `min`, `max`, `allowed` (pipe-separated) and `required` columns and the
rules are the dictionary; leave them out and only the name and column-set
checks run. One file describes the data for validation and for labelling, so
the two cannot drift.

## Three decisions that shape the output

**Missing is not wrong, unless the variable is required.** A blank in a
skip-pattern question is correct data. Only variables in `required` are flagged
for blanks; every other check ignores NA. The opposite policy, which the
previous version of this folder had, produces hundreds of false flags and
teaches people to ignore the report.

**Sentinel codes are missing.** -999, -99 and the rest arrive from ODK and
Stata as numbers. A range check that does not know that reports every refusal
as an age of -999. `Rules.sentinels` lists them and defaults to the common set;
pass `sentinels=[]` if the codes are meaningful in your instrument.

**Everything is reported by identifier, never by row number.** A row number
changes when the file is re-sorted; an id is what you phone the field team
with. The one exception is a blank id, which has nothing to be reported by,
and the message says so.

## Companions

`companions/validate.do` and `companions/validate.R` run the same duplicate,
required, range and allowed checks against the same dictionary, for a team
that works in Stata or R. They are not tested in CI (Stata has no free runtime)
and they do fewer things than the Python; the Python is the reference.

## What this replaced

Three scripts that printed `df[~df.gender.isin(["M", "F"])]` and stopped, in
three languages, plus a second folder under `foundation_tools/` with a
different set of five-line functions that overlapped with the first. Neither
reported an id, neither knew about sentinels, and neither could be pointed at a
new file without editing the source.
