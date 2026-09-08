# LaTeX

A quick-start template for a report, and notes on where LaTeX is worth the
learning curve for a development researcher.

| File | What it is |
|---|---|
| `quick_start_template.tex` | A report skeleton: title, abstract, sections, a table, a figure, a bibliography stub. Compiles with `pdflatex` and nothing else installed |
| `field_use_case_latex.md` | Where it has earned its place in this line of work |
| `community_links_latex.txt` | Where to ask |

## When to use it

A document with many numbered equations, a document with fifty tables that
have to look identical, or anything going to a journal that supplies a class
file. And a working paper where the bibliography is a `.bib` file that will
be reused: BibTeX is the reason to learn LaTeX, and it pays back on the
second paper.

## When not to

A report co-written with a programme team. Word's track changes is how most
of the sector reviews a document, and a LaTeX source is unreadable to a
reviewer who does not write it. Overleaf softens this and does not remove it.
For a donor report, a policy brief, or anything a non-technical colleague
must edit, use Word or Quarto, which renders to Word.

Quarto is the middle option: Markdown with code chunks, rendering to PDF
through LaTeX when you want that and to Word when you do not. FieldStack's
`notebooks/` and `automated_reporting/` are Quarto.

## What goes wrong

Tables. A regression table pasted from Stata or R into LaTeX by hand is
wrong by the third revision. Use `esttab` in Stata or `modelsummary` in R to
write the `.tex` directly, and `\input` it, so the table in the paper is the
table the code produced.

Fonts for Indic scripts need `xelatex` or `lualatex` rather than `pdflatex`,
and a font that has the script. `pdflatex` will compile a document with
Hindi in it and print boxes.
