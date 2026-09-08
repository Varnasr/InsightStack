"""Tests for label_variables. Run: python label_variables/test_label_variables.py

The check that matters is the round trip: labels written into a .dta come back
out of it. A label that lives only in `df.attrs` is one that vanishes the first
time somebody saves to CSV, which is what the previous version of this folder
did on the line after applying them.
"""

import sys
import tempfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from label_variables import (apply_labels, coverage, dictionary_from_file,  # noqa: E402
                             read_dictionary, write_labelled)

HERE = Path(__file__).resolve().parent
PASSED = 0


def check(cond, label):
    global PASSED
    if not cond:
        raise AssertionError(label)
    PASSED += 1


def frame():
    return pd.DataFrame({"id": ["H1", "H2", "H3"], "age": [34, 41, 29],
                         "gender": [1, 2, 3], "income": [1000.0, 2500.5, 800.0],
                         "consent": [1, 1, -99]})


def test_dictionary_reads_and_parses_value_labels():
    d = read_dictionary(HERE / "input" / "data_dictionary.csv")
    check(d["variable"].tolist() == ["id", "age", "gender", "income", "consent"], "variables")
    g = d.set_index("variable")["values"]["gender"]
    check(g == {1: "Male", 2: "Female", 3: "Other"}, "codes parsed as integers")
    c = d.set_index("variable")["values"]["consent"]
    check(c[-99] == "Refused", "negative code parsed")
    check(d.set_index("variable")["values"]["age"] == {}, "no values is an empty dict")


def test_duplicate_dictionary_entries_are_refused():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "d.csv"
        p.write_text("variable,label\nage,A\nage,B\n")
        try:
            read_dictionary(p)
        except ValueError as exc:
            check("listed twice" in str(exc), "duplicate refused")
        else:
            raise AssertionError("duplicate should be refused")


def test_coverage_reports_both_directions():
    d = read_dictionary(HERE / "input" / "data_dictionary.csv")
    df = frame().drop(columns=["consent"]); df["extra"] = 1
    cov = coverage(df, d).set_index("variable")["status"]
    check(cov["extra"] == "no dictionary entry", "column without an entry")
    check(cov["consent"] == "no such column", "entry without a column")
    check(cov["age"] == "labelled", "the ordinary case")


def test_apply_puts_labels_in_attrs_and_strict_refuses_gaps():
    d = read_dictionary(HERE / "input" / "data_dictionary.csv")
    out, cov = apply_labels(frame(), d)
    check(out.attrs["variable_labels"]["age"] == "Age in completed years", "variable label")
    check(out.attrs["value_labels"]["gender"][2] == "Female", "value label")
    check((cov["status"] == "labelled").all(), "everything labelled")
    df = frame(); df["extra"] = 1
    try:
        apply_labels(df, d, strict=True)
    except ValueError as exc:
        check("extra" in str(exc), "strict mode names the gap")
    else:
        raise AssertionError("strict should refuse an unlabelled column")


def test_labels_round_trip_through_stata():
    d = read_dictionary(HERE / "input" / "data_dictionary.csv")
    with tempfile.TemporaryDirectory() as tmp:
        p = write_labelled(frame(), Path(tmp) / "out.dta", dictionary=d)
        back = dictionary_from_file(p).set_index("variable")
        check(back.loc["age", "label"] == "Age in completed years", "variable label survives")
        check("2=Female" in back.loc["gender", "values"], "value label survives")
        check("-99=Refused" in back.loc["consent", "values"], "negative code survives")
        import pyreadstat
        df2, meta = pyreadstat.read_dta(str(p), apply_value_formats=True)
        check(df2["gender"].tolist() == ["Male", "Female", "Other"], "Stata applies the labels")


def test_labels_round_trip_through_spss():
    d = read_dictionary(HERE / "input" / "data_dictionary.csv")
    with tempfile.TemporaryDirectory() as tmp:
        p = write_labelled(frame(), Path(tmp) / "out.sav", dictionary=d)
        back = dictionary_from_file(p).set_index("variable")
        check(back.loc["income", "label"] == "Monthly income in INR", "sav variable label")
        check("1=Yes" in back.loc["consent", "values"], "sav value label")


def test_stata_limits_are_errors_not_truncation():
    d = read_dictionary(HERE / "input" / "data_dictionary.csv")
    with tempfile.TemporaryDirectory() as tmp:
        df = frame().rename(columns={"income": "a_variable_name_that_is_far_too_long_for_stata"})
        try:
            write_labelled(df, Path(tmp) / "x.dta", dictionary=d)
        except ValueError as exc:
            check("32 characters" in str(exc), "long name refused")
        else:
            raise AssertionError("should refuse a 45-character name")
        d2 = d.copy(); d2.loc[d2.variable == "age", "label"] = "x" * 81
        try:
            write_labelled(frame(), Path(tmp) / "y.dta", dictionary=d2)
        except ValueError as exc:
            check("80 characters" in str(exc), "long label refused")
        else:
            raise AssertionError("should refuse an 81-character label")


def test_csv_export_is_refused_with_an_explanation():
    try:
        write_labelled(frame(), "out.csv")
    except ValueError as exc:
        check("cannot carry labels" in str(exc), "CSV refused, reason given")
    else:
        raise AssertionError("CSV should be refused")


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in tests:
        fn(); print(f"  ok  {fn.__name__}")
    print(f"\n{len(tests)} tests, {PASSED} checks, all passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
