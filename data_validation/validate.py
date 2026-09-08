"""Rule-driven validation of a tabular file, with an issue row per problem.

Design notes, so the choices survive a refactor.

**Rules are data, not code.** A `Rules` object can be built from a data
dictionary CSV as easily as in Python, which is the point: the person who knows
that household size cannot exceed 30 in this survey is usually not the person
writing Python. `Rules.from_csv` reads the same dictionary that
`label_variables/` uses, so one file describes the data for both.

**Missing is not wrong, unless the variable is required.** A blank in a skip-
pattern question is correct data. Only variables listed in `required` are
flagged for blanks; a range or allowed-values check silently ignores NA. This
is the opposite of what a naive check does, and the naive check produces
hundreds of false flags that teach people to ignore the report.

**Sentinel codes are missing too.** -999, -99, 98, 99 arrive from ODK and Stata
as numbers, and a range check that does not know that reports every refusal as
an out-of-range age. `Rules.sentinels` lists them; the default covers the usual
conventions.

**The id is reported, never the row number.** A row number changes when the
file is re-sorted; an id is what you phone the field team with.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

__all__ = ["Rules", "Report", "validate", "check_cross_file_ids"]

_NAME_STYLES = {
    "snake_case": re.compile(r"^[a-z][a-z0-9_]*$"),
    "stata": re.compile(r"^[A-Za-z_][A-Za-z0-9_]{0,31}$"),
    "any": re.compile(r"^.+$"),
}

_TYPE_CHECKS = ("numeric", "integer", "date", "text", "binary")


@dataclass
class Rules:
    """What a valid file looks like.

    Parameters
    ----------
    id
        Identifier column. Checked for blanks and duplicates, and used to name
        every issue. Required.
    required
        Columns that must never be blank.
    ranges
        ``{column: (min, max)}``, either end ``None`` for open.
    allowed
        ``{column: [values]}``. Compared as strings after trimming, so ``1``
        and ``"1"`` match; case is significant.
    types
        ``{column: "numeric" | "integer" | "date" | "text" | "binary"}``.
        A column whose values cannot all be read as that type is reported per
        offending value, not per column, so you can see whether it is one
        stray entry or a wrong column.
    names
        ``"snake_case"``, ``"stata"`` (32 chars, letters/digits/underscore)
        or ``"any"``.
    sentinels
        Numeric codes that mean missing. Treated as blank everywhere.
    expected_columns
        If given, columns present in the file but not listed are reported,
        and listed columns absent from the file are reported. Catches a
        renamed question between survey rounds.
    """
    id: str
    required: list[str] = field(default_factory=list)
    ranges: dict[str, tuple] = field(default_factory=dict)
    allowed: dict[str, list] = field(default_factory=dict)
    types: dict[str, str] = field(default_factory=dict)
    names: str = "any"
    sentinels: list = field(default_factory=lambda: [-999, -998, -99, -88, -9])
    expected_columns: list[str] | None = None

    def __post_init__(self):
        if self.names not in _NAME_STYLES:
            raise ValueError(f"Rules.names must be one of {sorted(_NAME_STYLES)}")
        bad = {c: t for c, t in self.types.items() if t not in _TYPE_CHECKS}
        if bad:
            raise ValueError(f"Rules.types: unknown type(s) {bad}; use {_TYPE_CHECKS}")
        for c, r in self.ranges.items():
            if len(r) != 2:
                raise ValueError(f"Rules.ranges[{c!r}] must be (min, max)")
            lo, hi = r
            if lo is not None and hi is not None and lo > hi:
                raise ValueError(f"Rules.ranges[{c!r}]: min {lo} exceeds max {hi}")

    @classmethod
    def from_csv(cls, path, *, id: str, names: str = "any", **overrides) -> "Rules":
        """Build rules from a data dictionary.

        Expects columns ``variable`` and optionally ``type``, ``min``, ``max``,
        ``allowed`` (pipe-separated), ``required`` (yes/no). Missing columns
        are simply not used, so the `label_variables/` dictionary with only
        ``variable`` and ``label`` works and produces name checks alone.
        """
        d = pd.read_csv(path, dtype=str).fillna("")
        if "variable" not in d.columns:
            raise ValueError(f"{path}: a data dictionary needs a 'variable' column")
        d["variable"] = d["variable"].str.strip()
        req, ranges, allowed, types = [], {}, {}, {}
        for _, row in d.iterrows():
            v = row["variable"]
            if not v:
                continue
            if row.get("required", "").strip().lower() in ("yes", "y", "true", "1"):
                req.append(v)
            lo = row.get("min", "").strip(); hi = row.get("max", "").strip()
            if lo or hi:
                ranges[v] = (float(lo) if lo else None, float(hi) if hi else None)
            if row.get("allowed", "").strip():
                allowed[v] = [x.strip() for x in row["allowed"].split("|") if x.strip()]
            t = row.get("type", "").strip().lower()
            if t in _TYPE_CHECKS:
                types[v] = t
        kwargs = dict(id=id, required=req, ranges=ranges, allowed=allowed,
                      types=types, names=names,
                      expected_columns=d["variable"][d["variable"] != ""].tolist())
        kwargs.update(overrides)
        return cls(**kwargs)


_COLUMNS = ["check", "severity", "id", "variable", "value", "message"]


@dataclass
class Report:
    issues: pd.DataFrame
    n_rows: int
    n_columns: int

    @property
    def ok(self) -> bool:
        return self.issues.empty

    def summary(self) -> pd.DataFrame:
        if self.issues.empty:
            return pd.DataFrame(columns=["check", "severity", "n"])
        out = (self.issues.groupby(["check", "severity"]).size()
               .reset_index(name="n").sort_values(["severity", "n"], ascending=[True, False]))
        return out.reset_index(drop=True)

    def by_variable(self) -> pd.DataFrame:
        if self.issues.empty:
            return pd.DataFrame(columns=["variable", "n"])
        return (self.issues.groupby("variable").size().reset_index(name="n")
                .sort_values("n", ascending=False).reset_index(drop=True))

    def __repr__(self) -> str:
        if self.ok:
            return f"Report: {self.n_rows} rows, {self.n_columns} columns, no issues"
        return (f"Report: {self.n_rows} rows, {self.n_columns} columns, "
                f"{len(self.issues)} issues\n{self.summary().to_string(index=False)}")


def _issue(check, severity, ids, variable, values, message) -> pd.DataFrame:
    ids = list(ids)
    values = list(values) if not isinstance(values, str) and values is not None else [values] * len(ids)
    return pd.DataFrame({"check": check, "severity": severity,
                         "id": [str(i) for i in ids], "variable": variable,
                         "value": [None if v is None else str(v) for v in values],
                         "message": message}, columns=_COLUMNS)


def _blank_mask(s: pd.Series, sentinels) -> pd.Series:
    """True where a value should be treated as missing."""
    m = s.isna()
    if pd.api.types.is_numeric_dtype(s):
        return m | s.isin(sentinels)
    # Anything else is treated as text. Not `dtype == object`: pandas 3 gives
    # string columns its own `str` dtype, and a check keyed on object silently
    # skips every blank in every text column, which is what shipped first.
    t = s.astype(str).str.strip()
    m = m | t.isin(["", ".", "NA", "N/A", "n/a", "nan", "NaN", "None", "<NA>"])
    num = pd.to_numeric(t, errors="coerce")
    return m | num.isin(sentinels)


def validate(df: pd.DataFrame, rules: Rules) -> Report:
    """Apply every rule, return a Report with one issue row per problem."""
    if rules.id not in df.columns:
        raise KeyError(f"validate: no id column {rules.id!r} in the frame")

    parts: list[pd.DataFrame] = []
    ids = df[rules.id]

    # id: blanks and duplicates. A blank id cannot be reported by id, so the
    # row number is used there and only there, and the message says so.
    blank_id = _blank_mask(ids, rules.sentinels)
    if blank_id.any():
        parts.append(_issue("id_blank", "error",
                            [f"row {i}" for i in np.flatnonzero(blank_id)],
                            rules.id, None, "identifier is blank (reported by row number)"))
    dup = ids[~blank_id].astype(str).duplicated(keep=False)
    if dup.any():
        d = ids[~blank_id][dup].astype(str)
        counts = d.value_counts()
        parts.append(_issue("id_duplicate", "error", counts.index, rules.id, counts.values,
                            "identifier appears more than once"))

    # column set
    if rules.expected_columns is not None:
        expected = set(rules.expected_columns)
        present = set(df.columns)
        for c in sorted(expected - present):
            parts.append(_issue("column_missing", "error", ["(file)"], c, None,
                                "listed in the dictionary but absent from the file"))
        for c in sorted(present - expected - {rules.id}):
            parts.append(_issue("column_unexpected", "warning", ["(file)"], c, None,
                                "present in the file but not in the dictionary"))

    # names
    pat = _NAME_STYLES[rules.names]
    for c in df.columns:
        if not pat.match(str(c)):
            parts.append(_issue("name_style", "warning", ["(file)"], c, c,
                                f"column name does not follow {rules.names}"))

    # required
    for c in rules.required:
        if c not in df.columns:
            parts.append(_issue("column_missing", "error", ["(file)"], c, None,
                                "required column is absent"))
            continue
        m = _blank_mask(df[c], rules.sentinels)
        if m.any():
            parts.append(_issue("required_blank", "error", ids[m], c, None,
                                f"{c} is required but blank"))

    # types
    for c, t in rules.types.items():
        if c not in df.columns:
            continue
        s = df[c]
        m = ~_blank_mask(s, rules.sentinels)
        vals = s[m]
        if t in ("numeric", "integer", "binary"):
            num = pd.to_numeric(vals, errors="coerce")
            bad = num.isna()
            if t == "integer":
                bad = bad | (~bad & (num != np.floor(num)))
            if t == "binary":
                bad = bad | (~bad & ~num.isin([0, 1]))
            if bad.any():
                parts.append(_issue(f"type_{t}", "error", ids[m][bad], c, vals[bad],
                                    f"{c} should be {t}"))
        elif t == "date":
            parsed = pd.to_datetime(vals, errors="coerce", format="mixed")
            bad = parsed.isna()
            if bad.any():
                parts.append(_issue("type_date", "error", ids[m][bad], c, vals[bad],
                                    f"{c} is not a readable date"))
        # text: anything goes

    # ranges, ignoring blanks and non-numeric (reported by the type check if asked)
    for c, (lo, hi) in rules.ranges.items():
        if c not in df.columns:
            continue
        s = df[c]
        m = ~_blank_mask(s, rules.sentinels)
        num = pd.to_numeric(s[m], errors="coerce")
        ok = num.notna()
        out = pd.Series(False, index=num.index)
        if lo is not None:
            out = out | (ok & (num < lo))
        if hi is not None:
            out = out | (ok & (num > hi))
        if out.any():
            parts.append(_issue("out_of_range", "warning", ids[m][out], c, num[out],
                                f"{c} outside [{lo if lo is not None else '-inf'}, "
                                f"{hi if hi is not None else 'inf'}]"))

    # allowed values
    for c, allowed in rules.allowed.items():
        if c not in df.columns:
            continue
        s = df[c]
        m = ~_blank_mask(s, rules.sentinels)
        vals = s[m].astype(str).str.strip()
        allowed_s = {str(a).strip() for a in allowed}
        bad = ~vals.isin(allowed_s)
        if bad.any():
            parts.append(_issue("not_allowed", "error", ids[m][bad], c, vals[bad],
                                f"{c} not one of {sorted(allowed_s)}"))

    issues = (pd.concat(parts, ignore_index=True) if parts
              else pd.DataFrame(columns=_COLUMNS))
    sev = issues["severity"].map({"error": 0, "warning": 1}).fillna(2)
    issues = issues.assign(_s=sev).sort_values(["_s", "check", "variable", "id"]).drop(columns="_s")
    return Report(issues.reset_index(drop=True), len(df), df.shape[1])


def check_cross_file_ids(parent: pd.DataFrame, child: pd.DataFrame, *,
                         parent_id: str, child_key: str) -> pd.DataFrame:
    """Ids in a child file that have no parent, and parents with no children.

    A household roster with a member whose household id is not in the household
    file is either a typo or a lost household; either way the member's data
    cannot be joined and will drop silently at analysis. The second direction,
    a household with no members, is usually fine and is reported as a note.
    """
    for frame, col, name in ((parent, parent_id, "parent"), (child, child_key, "child")):
        if col not in frame.columns:
            raise KeyError(f"check_cross_file_ids: no column {col!r} in the {name} frame")
    p = set(parent[parent_id].dropna().astype(str))
    c = child[child_key].dropna().astype(str)
    orphans = c[~c.isin(p)]
    parts = []
    if not orphans.empty:
        counts = orphans.value_counts()
        parts.append(_issue("orphan_child", "error", counts.index, child_key, counts.values,
                            f"{child_key} not found in the parent file"))
    childless = sorted(p - set(c))
    if childless:
        parts.append(_issue("childless_parent", "note", childless, parent_id, None,
                            "no rows in the child file"))
    return pd.concat(parts, ignore_index=True) if parts else pd.DataFrame(columns=_COLUMNS)
