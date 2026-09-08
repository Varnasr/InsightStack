"""Tests for data_validation. Run: python data_validation/test_data_validation.py

Plain asserts and a main(), matching the other suites here. Each rule is tested
in both directions: that it fires on the case it exists for, and that it stays
quiet on the legitimate case that resembles it, because a validator that flags
every skip-pattern blank is one the team stops reading.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from data_validation import Rules, check_cross_file_ids, validate  # noqa: E402

HERE = Path(__file__).resolve().parent
PASSED = 0


def check(cond, label):
    global PASSED
    if not cond:
        raise AssertionError(label)
    PASSED += 1


def clean():
    return pd.DataFrame({
        "id": ["H1", "H2", "H3", "H4"],
        "age": [34, 41, 29, 55],
        "gender": ["M", "F", "F", "M"],
        "income": [1000.0, 2500.5, 800.0, 12000.0],
        "consent": ["yes", "yes", "yes", "yes"],
        "followup": ["a", None, None, None],           # skip pattern, mostly blank
    })


RULES = Rules(id="id", required=["consent"], ranges={"age": (0, 110), "income": (0, None)},
              allowed={"gender": ["M", "F", "O"]}, types={"age": "integer", "income": "numeric"},
              names="snake_case")


def test_clean_file_has_no_issues():
    r = validate(clean(), RULES)
    check(r.ok, "a clean file passes")
    check(len(r.issues) == 0, "and has no issue rows")


def test_skip_pattern_blanks_are_not_flagged():
    r = validate(clean(), RULES)
    check("followup" not in r.issues["variable"].tolist(), "unlisted blanks are fine")


def test_blank_required_is_flagged_for_empty_string_and_na_alike():
    df = clean(); df.loc[1, "consent"] = ""; df.loc[2, "consent"] = None
    r = validate(df, RULES)
    got = set(r.issues.loc[r.issues.check == "required_blank", "id"])
    check(got == {"H2", "H3"}, "both the empty string and the NA are reported by id")


def test_blank_detection_works_on_pandas_string_dtype():
    """pandas 3 gives text columns a `str` dtype, not object. The first
    version keyed on object and silently skipped every blank in every text
    column. This pins the fix on whichever pandas is installed."""
    df = clean()
    df["consent"] = pd.Series(["yes", "", "yes", "yes"], dtype="string")
    r = validate(df, RULES)
    check("H2" in r.issues.loc[r.issues.check == "required_blank", "id"].tolist(),
          "a blank in a string-dtype column is caught")


def test_duplicate_ids_report_the_id_and_the_count():
    df = clean(); df.loc[3, "id"] = "H2"
    r = validate(df, RULES)
    row = r.issues[r.issues.check == "id_duplicate"]
    check(len(row) == 1 and row.iloc[0]["id"] == "H2", "one row per duplicated id")
    check(row.iloc[0]["value"] == "2", "carrying the count")


def test_blank_id_is_reported_by_row_number_and_says_so():
    df = clean(); df.loc[2, "id"] = ""
    r = validate(df, RULES)
    row = r.issues[r.issues.check == "id_blank"].iloc[0]
    check(row["id"] == "row 2", "row number, since there is no id to use")
    check("row number" in row["message"], "and the message says why")


def test_sentinel_codes_count_as_missing_not_as_out_of_range():
    df = clean(); df.loc[0, "age"] = -999
    r = validate(df, RULES)
    check("out_of_range" not in r.issues["check"].tolist(), "-999 is missing, not a bad age")
    strict = Rules(id="id", ranges={"age": (0, 110)}, sentinels=[])
    r2 = validate(df, strict)
    check("out_of_range" in r2.issues["check"].tolist(), "unless sentinels are switched off")


def test_out_of_range_reports_the_value_and_ignores_blanks():
    df = clean(); df.loc[1, "age"] = 210; df.loc[2, "age"] = np.nan
    r = validate(df, RULES)
    rows = r.issues[r.issues.check == "out_of_range"]
    check(rows["id"].tolist() == ["H2"], "only the real violation")
    check(rows.iloc[0]["value"] == "210.0", "with the value")


def test_open_ended_range():
    df = clean(); df.loc[0, "income"] = -5
    r = validate(df, RULES)
    check("H1" in r.issues.loc[r.issues.variable == "income", "id"].tolist(),
          "min-only range catches a negative")
    df.loc[0, "income"] = 1e9
    check(validate(df, RULES).ok, "and has no upper bound")


def test_allowed_values_compare_as_trimmed_strings():
    df = clean(); df.loc[0, "gender"] = " F "; df.loc[1, "gender"] = "X"
    r = validate(df, RULES)
    bad = r.issues[r.issues.check == "not_allowed"]
    check(bad["id"].tolist() == ["H2"], "whitespace is forgiven, X is not")
    df2 = clean(); df2["gender"] = [1, 2, 1, 2]
    r2 = validate(df2, Rules(id="id", allowed={"gender": ["1", "2"]}))
    check(r2.ok, "an integer column matches string codes")


def test_type_checks_report_per_offending_value():
    df = clean(); df["age"] = [34, "forty", 29.5, 55]
    r = validate(df, RULES)
    bad = r.issues[r.issues.check == "type_integer"]
    check(set(bad["id"]) == {"H2", "H3"}, "the word and the non-integer, not the column")


def test_binary_and_date_types():
    df = clean(); df["consent"] = [1, 0, 2, 1]; df["dob"] = ["2001-04-05", "not a date", "1999-12-31", "2005-01-01"]
    r = validate(df, Rules(id="id", types={"consent": "binary", "dob": "date"}))
    check(r.issues.loc[r.issues.check == "type_binary", "id"].tolist() == ["H3"], "2 is not binary")
    check(r.issues.loc[r.issues.check == "type_date", "id"].tolist() == ["H2"], "one unreadable date")


def test_name_style():
    df = clean().rename(columns={"income": "Monthly Income"})
    r = validate(df, RULES)
    check("Monthly Income" in r.issues.loc[r.issues.check == "name_style", "variable"].tolist(),
          "snake_case violation reported")
    check(validate(df, Rules(id="id", names="any")).ok, "and not when names are unconstrained")


def test_expected_columns_catch_a_renamed_question():
    df = clean().rename(columns={"income": "hh_income"})
    r = validate(df, Rules(id="id", expected_columns=["age", "gender", "income", "consent", "followup"]))
    checks = r.issues.set_index("variable")["check"].to_dict()
    check(checks.get("income") == "column_missing", "the old name is missing")
    check(checks.get("hh_income") == "column_unexpected", "the new name is unexpected")


def test_rules_from_a_data_dictionary():
    rules = Rules.from_csv(HERE / "sample_data" / "data_dictionary.csv", id="id", names="snake_case")
    check(rules.required == ["id", "age", "gender"], "required read from the yes column")
    check(rules.ranges["age"] == (0.0, 110.0), "range read from min/max")
    check(rules.ranges["income"] == (0.0, None), "open upper bound where max is blank")
    check(rules.allowed["gender"] == ["M", "F", "O"], "allowed split on |")
    check(rules.types["age"] == "integer", "type read")
    sample = pd.read_csv(HERE / "sample_data" / "sample_data.csv")
    r = validate(sample, rules)
    check(isinstance(r.n_rows, int) and r.n_rows == len(sample), "runs on the bundled sample")


def test_bad_rules_are_refused_at_construction():
    for kwargs, msg in ((dict(id="id", names="camel"), "names"),
                        (dict(id="id", types={"a": "float"}), "unknown type"),
                        (dict(id="id", ranges={"a": (10, 1)}), "exceeds")):
        try:
            Rules(**kwargs)
        except ValueError as exc:
            check(msg in str(exc), f"refused: {msg}")
        else:
            raise AssertionError(f"Rules({kwargs}) should have been refused")


def test_cross_file_ids():
    hh = pd.DataFrame({"hh_id": ["H1", "H2", "H3"]})
    members = pd.DataFrame({"hh_id": ["H1", "H1", "H2", "H9"]})
    out = check_cross_file_ids(hh, members, parent_id="hh_id", child_key="hh_id")
    check(out.loc[out.check == "orphan_child", "id"].tolist() == ["H9"], "the orphan")
    check(out.loc[out.check == "childless_parent", "id"].tolist() == ["H3"], "the childless household")
    check(out.loc[out.check == "orphan_child", "severity"].iloc[0] == "error", "orphan is an error")
    check(out.loc[out.check == "childless_parent", "severity"].iloc[0] == "note", "childless is a note")


def test_report_summary_and_ordering():
    df = clean(); df.loc[3, "id"] = "H2"; df.loc[0, "age"] = 300
    r = validate(df, RULES)
    check(r.issues["severity"].tolist()[0] == "error", "errors sort first")
    s = r.summary()
    check(set(s["check"]) == {"id_duplicate", "out_of_range"}, "summary counts by check")
    check("2 issues" in repr(r), "repr states the count")


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in tests:
        fn(); print(f"  ok  {fn.__name__}")
    print(f"\n{len(tests)} tests, {PASSED} checks, all passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
