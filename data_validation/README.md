# data_validation

Checks a data file against a data dictionary and lists every problem by
identifier.

```python
from data_validation import validate, Rules

rules = Rules.from_csv("sample_data/data_dictionary.csv", id="id", names="snake_case")
report = validate(df, rules)
report.issues        # one row per problem: id, variable, value, check, message
report.summary()     # counts by check and severity
report.ok            # True when nothing fired
```

```
python data_validation/test_data_validation.py    # 18 tests, 40 checks
```

## Checks

| Check | Fires when |
| --- | --- |
| `id_blank`, `id_duplicate` | The identifier is missing or repeated |
| `required_blank` | A required variable is blank, NA, `.`, or a sentinel code |
| `out_of_range` | A numeric value is outside the declared `(min, max)`; either end may be open |
| `not_allowed` | A value is not in the declared list |
| `type_numeric`, `type_integer`, `type_binary`, `type_date` | A value cannot be read as the declared type |
| `name_style` | A column name breaks `snake_case` or Stata's 32-character limit |
| `column_missing`, `column_unexpected` | The file's columns differ from the dictionary's |
| `orphan_child`, `childless_parent` | `check_cross_file_ids`: a roster row without a household, or the reverse |

## The dictionary

`Rules.from_csv` reads the dictionary that `label_variables/` also uses,
with `type`, `min`, `max`, `allowed` (pipe-separated) and `required`
columns. Without them, only the name and column-set checks run.

## Behaviour

Only variables listed in `required` are flagged for blanks. A blank in a
skip-pattern question is correct data.

Sentinel codes (-999, -99 and the rest) count as missing. `Rules.sentinels`
lists them; pass `sentinels=[]` if the codes mean something in your
instrument.

Problems are reported by identifier, not row number. A blank identifier is
the one exception, and the message says so.

## Companions

`companions/validate.do` and `companions/validate.R` run the duplicate,
required, range and allowed checks against the same dictionary in Stata and
R. They are not tested in CI and do less than the Python, which is the
reference.
