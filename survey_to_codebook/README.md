# survey_to_codebook

An XLSForm already contains everything a codebook needs, question by question.
This writes it out as one document a reviewer or analyst can read top to
bottom, and reports the defects it finds in the form on the way.

```
python -m survey_to_codebook input/survey.xlsx -o output/codebook.md --csv output/dictionary.csv
python survey_to_codebook/test_survey_to_codebook.py     # 9 tests, 27 checks
```

Exit status is 1 when the form has a problem, so it can gate a deployment.

## What the codebook records

For every variable: the export path (`group/question`, matching the column name
the platform will produce), type, label, hint, whether it is required, the
relevance expression it is asked under, its constraint, and for a select the
full choice list with codes. Metadata rows (`start`, `end`, `deviceid`,
`calculate`, `note`) are kept and marked, so a reader knows which columns in
the export are not answers.

The `--csv` output is a flat dictionary in the shape `label_variables/` reads,
with the choice lists as `code=label|...` value labels. So a form's own choices
become the value labels on its exported data, with nothing retyped.

## What it catches

| Problem | Why it matters |
|---|---|
| A select naming a choice list that is not on the choices sheet | The form will not deploy, and a codebook that silently prints an empty list hides why |
| A choice list no question uses | Usually a renamed question; the old list is a fossil |
| A group opened and never closed | Every later path is wrong |
| The same variable name twice | The export overwrites one column with the other |
| A group name written in the `type` cell (`begin_group personal`) with `name` blank | Some exports do this; both spellings are read |

The bundled `input/survey.xlsx` shipped with the first of these: the form said
`select_multiple hobbies` and the choices sheet named the list `hobby`. The
previous notebook printed a codebook with an empty choice list and no comment.
This tool reported it on the first run, and the sample is now fixed.

## What this replaced

A notebook that iterated the survey sheet and printed a heading per row. It did
not know about groups, so every path was wrong for a grouped question; it
handled `select_one` and not `select_multiple`; and it looked up choice lists
by splitting on whitespace and taking the second token, which works until a
list name has a space in it.
