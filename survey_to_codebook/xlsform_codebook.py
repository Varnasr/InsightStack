"""Read an XLSForm, resolve its structure, write a codebook.

Handles the parts of the format that a first attempt gets wrong:

- **Groups and repeats.** `begin_group` / `end_group` and `begin_repeat` /
  `end_repeat` nest, and the exported column name for a question inside them is
  `group/question`. The codebook records the path so it matches the export.
- **A group name written in the type cell.** Some exports carry
  `begin_group personal` in `type` with `name` blank. Both spellings are read.
- **select_one and select_multiple.** Each names a choice list; the list is
  looked up and every option listed. A select naming a list that does not
  exist is reported, since the form would fail to deploy and the codebook
  should say so rather than print an empty list.
- **Unused choice lists** are reported at the end, because a list nobody
  references is usually a renamed question.
- **Duplicate names** are refused, since the export would overwrite one column
  with another.
- **Metadata rows** (`start`, `end`, `deviceid`, `today`, `username`,
  `calculate`, `note`) are kept but marked, so a reader knows which columns in
  the export are not answers.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pandas as pd

__all__ = ["read_xlsform", "build_codebook", "to_markdown", "to_csv", "main"]

_STRUCTURE = {"begin_group", "end_group", "begin_repeat", "end_repeat", "begin group",
              "end group", "begin repeat", "end repeat"}
_META = {"start", "end", "today", "deviceid", "subscriberid", "simserial",
         "phonenumber", "username", "email", "audit", "calculate", "note", "hidden"}


def read_xlsform(path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return the survey and choices sheets as string frames, blanks as ''."""
    x = pd.ExcelFile(path)
    missing = [s for s in ("survey", "choices") if s not in x.sheet_names]
    if missing:
        raise ValueError(f"{path}: an XLSForm needs sheet(s) {missing}; found {x.sheet_names}")
    survey = x.parse("survey", dtype=str).fillna("")
    choices = x.parse("choices", dtype=str).fillna("")
    survey.columns = [str(c).strip() for c in survey.columns]
    choices.columns = [str(c).strip() for c in choices.columns]
    for col in ("type", "name"):
        if col not in survey.columns:
            raise ValueError(f"{path}: the survey sheet needs a {col!r} column")
    for col in ("list_name", "name"):
        if col not in choices.columns:
            raise ValueError(f"{path}: the choices sheet needs a {col!r} column")
    if "label" not in survey.columns:
        lab = [c for c in survey.columns if c.startswith("label")]
        if not lab:
            raise ValueError(f"{path}: the survey sheet has no label column")
        survey["label"] = survey[lab[0]]
    if "label" not in choices.columns:
        lab = [c for c in choices.columns if c.startswith("label")]
        choices["label"] = choices[lab[0]] if lab else ""
    return survey, choices


def _split_type(raw: str) -> tuple[str, str]:
    """``"select_one gender"`` to ``("select_one", "gender")``; plain types to ``(t, "")``."""
    parts = str(raw).strip().split()
    if not parts:
        return "", ""
    head = parts[0].lower()
    if head in ("begin", "end") and len(parts) > 1 and parts[1].lower() in ("group", "repeat"):
        head = f"{head}_{parts[1].lower()}"
        rest = " ".join(parts[2:])
    else:
        rest = " ".join(parts[1:])
    return head, rest.strip()


def build_codebook(survey: pd.DataFrame, choices: pd.DataFrame) -> dict:
    """Resolve the form into entries. Returns ``{"entries": [...], "problems": [...]}``."""
    lists: dict[str, list] = {}
    for _, row in choices.iterrows():
        ln = str(row["list_name"]).strip()
        if ln:
            lists.setdefault(ln, []).append((str(row["name"]).strip(), str(row.get("label", "")).strip()))

    entries, problems, stack, seen = [], [], [], {}
    used_lists = set()

    def col(row, name):
        return str(row[name]).strip() if name in row.index else ""

    for i, row in survey.iterrows():
        kind, rest = _split_type(row["type"])
        name = col(row, "name")
        if not kind:
            continue
        if kind in ("begin_group", "begin_repeat"):
            gname = name or rest
            if not gname:
                problems.append(f"row {i + 2}: {kind} with no name")
                gname = f"unnamed_{i + 2}"
            stack.append((gname, kind == "begin_repeat"))
            continue
        if kind in ("end_group", "end_repeat"):
            if stack:
                stack.pop()
            else:
                problems.append(f"row {i + 2}: {kind} with nothing open")
            continue
        if not name:
            problems.append(f"row {i + 2}: {kind} question with no name")
            continue

        path = "/".join([g for g, _ in stack] + [name])
        if name in seen:
            raise ValueError(f"survey sheet: variable name {name!r} appears twice "
                             f"(rows {seen[name]} and {i + 2}); the export would overwrite one")
        seen[name] = i + 2

        entry = {
            "name": name, "path": path, "type": kind,
            "label": col(row, "label"),
            "hint": col(row, "hint"),
            "required": col(row, "required").lower() in ("yes", "true", "true()", "1"),
            "relevant": col(row, "relevant"),
            "constraint": col(row, "constraint"),
            "constraint_message": col(row, "constraint_message"),
            "in_repeat": any(r for _, r in stack),
            "is_metadata": kind in _META,
            "choices": [],
            "list_name": "",
        }
        if kind in ("select_one", "select_multiple", "select_one_from_file", "rank"):
            ln = rest.split()[0] if rest else ""
            entry["list_name"] = ln
            if ln in lists:
                entry["choices"] = lists[ln]
                used_lists.add(ln)
            elif kind != "select_one_from_file":
                problems.append(f"{path}: {kind} names choice list {ln!r}, which is not on the choices sheet")
        entries.append(entry)

    if stack:
        problems.append(f"{len(stack)} group(s) never closed: {[g for g, _ in stack]}")
    for ln in lists:
        if ln not in used_lists:
            problems.append(f"choice list {ln!r} is defined but no question uses it")
    return {"entries": entries, "problems": problems}


def to_markdown(codebook: dict, *, title: str = "Codebook") -> str:
    e = codebook["entries"]
    n_q = sum(1 for x in e if not x["is_metadata"])
    out = [f"# {title}", "",
           f"{len(e)} variables, of which {n_q} are questions and {len(e) - n_q} are "
           "form metadata or calculations.", ""]
    out += ["| Variable | Type | Label |", "|---|---|---|"]
    for x in e:
        tag = " *(metadata)*" if x["is_metadata"] else (" *(in repeat)*" if x["in_repeat"] else "")
        out.append(f"| `{x['path']}` | {x['type']} | {x['label']}{tag} |")
    out.append("")
    for x in e:
        out.append(f"## `{x['path']}`")
        out.append("")
        out.append(f"**{x['label'] or '(no label)'}**  ")
        out.append(f"Type: `{x['type']}`" + (f" from list `{x['list_name']}`" if x["list_name"] else "")
                   + ("; required" if x["required"] else "") + ("; inside a repeat" if x["in_repeat"] else "")
                   + "  ")
        if x["hint"]:
            out.append(f"Hint: {x['hint']}  ")
        if x["relevant"]:
            out.append(f"Asked when: `{x['relevant']}`  ")
        if x["constraint"]:
            msg = f" ({x['constraint_message']})" if x["constraint_message"] else ""
            out.append(f"Constraint: `{x['constraint']}`{msg}  ")
        if x["choices"]:
            out.append("")
            out.append("| Code | Label |"); out.append("|---|---|")
            out += [f"| `{c}` | {l} |" for c, l in x["choices"]]
        if x["type"] == "select_multiple":
            out.append("")
            out.append("Exported as one space-separated string of selected codes; "
                       "expand to one column per option before tabulating.")
        out.append("")
    if codebook["problems"]:
        out += ["## Problems found in the form", ""]
        out += [f"- {p}" for p in codebook["problems"]]
        out.append("")
    return "\n".join(out)


def to_csv(codebook: dict) -> pd.DataFrame:
    """A flat frame, one row per variable, choices joined as ``code=label|...``.

    This is the shape `label_variables/` reads, so a codebook made here can be
    applied straight back onto the exported data as labels.
    """
    rows = []
    for x in codebook["entries"]:
        rows.append({"variable": x["name"], "path": x["path"], "type": x["type"],
                     "label": x["label"],
                     "values": "|".join(f"{c}={l}" for c, l in x["choices"]),
                     "required": "yes" if x["required"] else "no",
                     "relevant": x["relevant"], "constraint": x["constraint"],
                     "metadata": "yes" if x["is_metadata"] else "no"})
    return pd.DataFrame(rows)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="XLSForm to Markdown codebook")
    ap.add_argument("xlsform")
    ap.add_argument("-o", "--output", default=None, help="markdown path (default: stdout)")
    ap.add_argument("--csv", default=None, help="also write a flat CSV dictionary here")
    ap.add_argument("--title", default="Codebook")
    args = ap.parse_args(argv)
    survey, choices = read_xlsform(args.xlsform)
    book = build_codebook(survey, choices)
    md = to_markdown(book, title=args.title)
    if args.output:
        Path(args.output).write_text(md, encoding="utf-8")
        print(f"wrote {args.output}: {len(book['entries'])} variables, {len(book['problems'])} problem(s)")
    else:
        sys.stdout.write(md)
    if args.csv:
        to_csv(book).to_csv(args.csv, index=False)
        print(f"wrote {args.csv}")
    return 1 if book["problems"] else 0


if __name__ == "__main__":
    sys.exit(main())
