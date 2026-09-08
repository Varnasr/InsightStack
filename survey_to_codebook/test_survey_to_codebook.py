"""Tests for survey_to_codebook. Run: python survey_to_codebook/test_survey_to_codebook.py

The fixture XLSForm is built in code with openpyxl, so the test does not depend
on the bundled example and can exercise the awkward cases on purpose: a group
name written in the type cell, a select naming a list that does not exist, a
choice list nobody uses, a repeat, and a duplicate variable name.
"""

import sys
import tempfile
from pathlib import Path

import openpyxl

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from survey_to_codebook import build_codebook, read_xlsform, to_csv, to_markdown  # noqa: E402

HERE = Path(__file__).resolve().parent
PASSED = 0


def check(cond, label):
    global PASSED
    if not cond:
        raise AssertionError(label)
    PASSED += 1


def write_form(path, survey_rows, choices_rows,
               survey_cols=("type", "name", "label", "hint", "relevant", "constraint", "required")):
    wb = openpyxl.Workbook()
    ws = wb.active; ws.title = "survey"
    ws.append(list(survey_cols))
    for r in survey_rows:
        ws.append(list(r) + [""] * (len(survey_cols) - len(r)))
    wc = wb.create_sheet("choices")
    wc.append(["list_name", "name", "label"])
    for r in choices_rows:
        wc.append(list(r))
    wb.save(path)
    return path


def standard_form(path):
    return write_form(path, [
        ("start", "start", ""),
        ("begin_group", "hh", "Household"),
        ("text", "head_name", "Name of household head", "Full name", "", "", "yes"),
        ("integer", "hh_size", "Household size", "", "", ". >= 1 and . <= 30", "yes"),
        ("select_one gender", "head_sex", "Sex of head"),
        ("begin_repeat", "member", "Household member"),
        ("integer", "age", "Age", "In completed years", "", ". >= 0"),
        ("select_multiple asset", "owns", "Assets owned", "", "${age} >= 18"),
        ("end_repeat", "", ""),
        ("end_group", "", ""),
        ("note", "thanks", "Thank you"),
    ], [
        ("gender", "m", "Male"), ("gender", "f", "Female"),
        ("asset", "1", "Bicycle"), ("asset", "2", "Phone"), ("asset", "3", "Land"),
    ])


def test_paths_follow_groups_and_repeats():
    with tempfile.TemporaryDirectory() as tmp:
        survey, choices = read_xlsform(standard_form(Path(tmp) / "f.xlsx"))
        book = build_codebook(survey, choices)
        paths = {e["name"]: e["path"] for e in book["entries"]}
        check(paths["head_name"] == "hh/head_name", "group prefix")
        check(paths["age"] == "hh/member/age", "nested repeat prefix")
        check(paths["start"] == "start", "top-level metadata has no prefix")
        rep = {e["name"]: e["in_repeat"] for e in book["entries"]}
        check(rep["age"] and not rep["hh_size"], "in_repeat is set only inside the repeat")
        check(book["problems"] == [], "a well-formed form has no problems")


def test_choices_are_resolved_and_required_and_relevance_kept():
    with tempfile.TemporaryDirectory() as tmp:
        survey, choices = read_xlsform(standard_form(Path(tmp) / "f.xlsx"))
        e = {x["name"]: x for x in build_codebook(survey, choices)["entries"]}
        check(e["head_sex"]["choices"] == [("m", "Male"), ("f", "Female")], "select_one list")
        check(len(e["owns"]["choices"]) == 3, "select_multiple list")
        check(e["hh_size"]["required"] and not e["age"]["required"], "required parsed")
        check(e["owns"]["relevant"] == "${age} >= 18", "relevance kept")
        check(e["hh_size"]["constraint"] == ". >= 1 and . <= 30", "constraint kept")
        check(e["start"]["is_metadata"] and e["thanks"]["is_metadata"], "metadata flagged")


def test_group_name_in_the_type_cell_is_read():
    """Some exports write `begin_group personal` in type and leave name blank."""
    with tempfile.TemporaryDirectory() as tmp:
        p = write_form(Path(tmp) / "f.xlsx",
                       [("begin_group personal", "", ""), ("text", "name", "Name"), ("end_group", "", "")], [])
        survey, choices = read_xlsform(p)
        book = build_codebook(survey, choices)
        check(book["entries"][0]["path"] == "personal/name", "group name recovered from the type cell")
        check(book["problems"] == [], "and not reported as a problem")


def test_missing_and_unused_choice_lists_are_reported():
    with tempfile.TemporaryDirectory() as tmp:
        p = write_form(Path(tmp) / "f.xlsx",
                       [("select_one colour", "fav", "Favourite colour")],
                       [("size", "s", "Small"), ("size", "l", "Large")])
        survey, choices = read_xlsform(p)
        book = build_codebook(survey, choices)
        msgs = " ".join(book["problems"])
        check("'colour'" in msgs and "not on the choices sheet" in msgs, "missing list reported")
        check("'size'" in msgs and "no question uses it" in msgs, "unused list reported")
        check(book["entries"][0]["choices"] == [], "and the entry has no choices rather than wrong ones")


def test_unclosed_group_is_reported():
    with tempfile.TemporaryDirectory() as tmp:
        p = write_form(Path(tmp) / "f.xlsx", [("begin_group", "g", "G"), ("text", "q", "Q")], [])
        survey, choices = read_xlsform(p)
        book = build_codebook(survey, choices)
        check(any("never closed" in m for m in book["problems"]), "unclosed group reported")


def test_duplicate_variable_name_is_refused():
    with tempfile.TemporaryDirectory() as tmp:
        p = write_form(Path(tmp) / "f.xlsx", [("text", "q", "Q1"), ("integer", "q", "Q2")], [])
        survey, choices = read_xlsform(p)
        try:
            build_codebook(survey, choices)
        except ValueError as exc:
            check("appears twice" in str(exc), "duplicate name refused")
        else:
            raise AssertionError("duplicate should be refused")


def test_markdown_and_csv_outputs():
    with tempfile.TemporaryDirectory() as tmp:
        survey, choices = read_xlsform(standard_form(Path(tmp) / "f.xlsx"))
        book = build_codebook(survey, choices)
        md = to_markdown(book, title="Test form")
        check(md.startswith("# Test form"), "title")
        check("| `hh/member/owns` | select_multiple |" in md, "summary table row")
        check("space-separated string" in md, "select_multiple export note")
        check("| `2` | Phone |" in md, "choice rows")
        csv = to_csv(book).set_index("variable")
        check(csv.loc["owns", "values"] == "1=Bicycle|2=Phone|3=Land", "csv values in label_variables format")
        check(csv.loc["hh_size", "required"] == "yes", "csv required")
        check(csv.loc["start", "metadata"] == "yes", "csv metadata flag")


def test_bundled_example_runs():
    survey, choices = read_xlsform(HERE / "input" / "survey.xlsx")
    book = build_codebook(survey, choices)
    check(any(e["path"] == "personal/gender" for e in book["entries"]), "bundled form parses")


def test_missing_sheet_is_a_clear_error():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "bad.xlsx"
        wb = openpyxl.Workbook(); wb.active.title = "survey"; wb.active.append(["type", "name"]); wb.save(p)
        try:
            read_xlsform(p)
        except ValueError as exc:
            check("choices" in str(exc), "names the missing sheet")
        else:
            raise AssertionError("should refuse a form with no choices sheet")


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in tests:
        fn(); print(f"  ok  {fn.__name__}")
    print(f"\n{len(tests)} tests, {PASSED} checks, all passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
