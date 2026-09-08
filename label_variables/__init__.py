"""Variable and value labels from a data dictionary, applied and written out.

    from label_variables import read_dictionary, apply_labels, write_labelled

    dictionary = read_dictionary("input/data_dictionary.csv")
    df, coverage = apply_labels(df, dictionary)
    write_labelled(df, "out/survey.dta")       # labels travel into Stata
    write_labelled(df, "out/survey.sav")       # or SPSS

A CSV has no labels, so a dataset that lives as CSV loses them on every
round-trip. Stata and SPSS files carry them, which is why the export functions
here matter more than the apply step. The version this replaced stored labels
in `df.attrs` and wrote a CSV, which discards them on the same line.
"""

from .labels import (apply_labels, coverage, dictionary_from_file, read_dictionary,
                     write_labelled)

__all__ = ["read_dictionary", "apply_labels", "coverage", "write_labelled",
           "dictionary_from_file"]
