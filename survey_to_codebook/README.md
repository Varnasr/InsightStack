# survey_to_codebook

Writes a codebook from an XLSForm, one document a reviewer can read top to
bottom, and reports defects in the form.

```
python -m survey_to_codebook input/survey.xlsx -o output/codebook.md --csv output/dictionary.csv
python survey_to_codebook/test_survey_to_codebook.py     # 9 tests, 27 checks
```

Exit status is 1 when the form has a problem.

## Output

For every variable: the export path (`group/question`, matching the column
name the platform produces), type, label, hint, whether it is required, its
relevance expression, its constraint, and for a select the full choice list
with codes. Metadata rows (`start`, `end`, `deviceid`, `calculate`, `note`)
are kept and marked.

`--csv` writes a flat dictionary in the shape `label_variables/` reads, with
choice lists as `code=label|...` value labels.

## Defects reported

| Problem | Effect |
| --- | --- |
| A select names a choice list not on the choices sheet | The form will not deploy |
| A choice list no question uses | Usually a renamed question |
| A group opened and never closed | Every later path is wrong |
| The same variable name twice | The export overwrites one column with the other |
| A group name in the `type` cell (`begin_group personal`) with `name` blank | Read either way |

The bundled `input/survey.xlsx` once had the first of these (`select_multiple
hobbies` against a list named `hobby`); it is fixed.
