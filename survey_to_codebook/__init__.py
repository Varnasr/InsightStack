"""XLSForm to codebook: the documentation the form already contains, written down.

    python -m survey_to_codebook input/survey.xlsx -o output/codebook.md

An XLSForm carries everything a codebook needs, question by question: the
variable name, the label, the type, the choice list, the skip logic, the
constraint, the hint. Almost nobody reads it as a codebook because it is a
spreadsheet with the choices on a different sheet. This turns it into one
document a reviewer or an analyst can read top to bottom.
"""

from .xlsform_codebook import build_codebook, read_xlsform, to_csv, to_markdown

__all__ = ["read_xlsform", "build_codebook", "to_markdown", "to_csv"]
