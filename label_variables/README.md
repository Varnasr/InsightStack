# label_variables

Variable and value labels from a data dictionary, applied to a frame and
written into a Stata or SPSS file.

```python
from label_variables import read_dictionary, apply_labels, write_labelled

d = read_dictionary("input/data_dictionary.csv")
df, cov = apply_labels(df, d)          # cov lists unlabelled variables and dictionary rows with no column
write_labelled(df, "out/survey.dta")
write_labelled(df, "out/survey.sav")
```

```
python label_variables/test_label_variables.py    # 8 tests, 20 checks
```

## The dictionary

```
variable,label,values
gender,Gender of respondent,1=Male|2=Female|3=Other
consent,Consent to interview,1=Yes|0=No|-99=Refused
```

`values` is optional and holds value labels as `code=label` pairs separated
by `|`. `data_validation/` reads the same file for its `min`, `max`,
`allowed` and `required` columns, and `survey_to_codebook/` writes this
shape from an XLSForm.

## Behaviour

`write_labelled` writes `.dta` or `.sav` and refuses `.csv`, which cannot
carry labels.

`dictionary_from_file` reads a labelled `.dta` or `.sav` and writes the
dictionary. The tests check the round trip in both formats.

Stata limits variable names to 32 characters and variable labels to 80.
`write_labelled` raises on either rather than truncating.

## Companions

`companions/label.do` and `companions/label.R` apply the same dictionary in
Stata and R. `label.do` builds `label define` statements from the `values`
column.
