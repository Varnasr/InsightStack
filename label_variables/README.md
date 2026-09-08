# label_variables

Variable and value labels from a data dictionary, applied to a frame and
written into a file that can carry them.

```python
from label_variables import read_dictionary, apply_labels, write_labelled

d = read_dictionary("input/data_dictionary.csv")
df, cov = apply_labels(df, d)          # cov says what is unlabelled, and what has no column
write_labelled(df, "out/survey.dta")   # labels are now in the file
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

`values` is optional and holds value labels as `code=label` pairs separated by
`|`. The same file serves `data_validation/`, which reads its `min`, `max`,
`allowed` and `required` columns; and `survey_to_codebook/` writes this exact
shape from an XLSForm, so a form's own choice lists become the value labels on
its export without retyping.

## Why the export step is the point

A CSV has no labels. A dataset that lives as CSV loses its labels on every
round-trip, and the previous version of this folder attached labels to
`df.attrs` and then wrote a CSV, which discards them on the same line. Stata
and SPSS files carry both variable and value labels in the file, so
`write_labelled` writes `.dta` or `.sav` and refuses `.csv` with an
explanation.

`dictionary_from_file` goes the other way: given a labelled `.dta` or `.sav`,
it emits the dictionary, so a file you were handed becomes a dictionary you
can keep. The tests check the round trip in both formats.

## Two Stata limits, enforced rather than truncated

Variable names are limited to 32 characters and variable labels to 80. The
writer would truncate silently; `write_labelled` raises instead, because a
truncated label reads as a mistake to whoever opens the file next.

## Companions

`companions/label.do` and `companions/label.R` apply the same dictionary in
Stata and R. `label.do` reads the `values` column and builds `label define`
statements from it, so the value labels come along, which the previous
Stata script did not do.
