"""Labels: read them from a dictionary, apply, report what is missing, write out.

The dictionary is a CSV with a ``variable`` column, a ``label`` column, and an
optional ``values`` column holding value labels as ``code=label`` pairs
separated by ``|``, for example ``1=Yes|0=No|-99=Refused``. The same file
serves `data_validation/`, which reads its ``min``, ``max``, ``allowed`` and
``required`` columns and ignores the rest, so one dictionary describes the
data for both.

Labels live in ``df.attrs["variable_labels"]`` and ``df.attrs["value_labels"]``
while in pandas, and are written into the file's own metadata by
`write_labelled`. pandas does not preserve ``attrs`` through most operations,
and that is fine: the dictionary is the source of truth, and `apply_labels`
is cheap to call again just before writing.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

__all__ = ["read_dictionary", "apply_labels", "coverage", "write_labelled",
           "dictionary_from_file"]


def _parse_values(spec: str) -> dict:
    """``"1=Yes|0=No"`` to ``{1: "Yes", 0: "No"}``. Numeric codes become numbers."""
    out = {}
    for pair in str(spec).split("|"):
        pair = pair.strip()
        if not pair:
            continue
        if "=" not in pair:
            raise ValueError(f"value label {pair!r} is not code=label")
        code, label = pair.split("=", 1)
        code = code.strip()
        try:
            code_v = int(code)
        except ValueError:
            try:
                code_v = float(code)
            except ValueError:
                code_v = code
        out[code_v] = label.strip()
    return out


def read_dictionary(path) -> pd.DataFrame:
    """Read and check a dictionary CSV. Returns variable, label, values (dict)."""
    d = pd.read_csv(path, dtype=str).fillna("")
    for col in ("variable", "label"):
        if col not in d.columns:
            raise ValueError(f"{path}: a data dictionary needs a {col!r} column")
    d["variable"] = d["variable"].str.strip()
    d = d[d["variable"] != ""].copy()
    dup = d["variable"][d["variable"].duplicated()]
    if not dup.empty:
        raise ValueError(f"{path}: variable(s) listed twice: {sorted(set(dup))}")
    d["label"] = d["label"].str.strip()
    d["values"] = (d["values"].map(_parse_values) if "values" in d.columns
                   else [dict() for _ in range(len(d))])
    return d[["variable", "label", "values"]].reset_index(drop=True)


def coverage(df: pd.DataFrame, dictionary: pd.DataFrame) -> pd.DataFrame:
    """One row per variable in either place, saying where it is and is not.

    A column with no dictionary entry ships unlabelled. A dictionary entry with
    no column is a renamed question, or a question dropped between rounds, and
    either way somebody should know. Both are listed; neither raises, because
    a partial dictionary is normal mid-cleaning.
    """
    cols = list(df.columns)
    dict_vars = dictionary["variable"].tolist()
    labels = dict(zip(dictionary["variable"], dictionary["label"]))
    rows = []
    for c in cols:
        rows.append({"variable": c, "in_data": True, "in_dictionary": c in labels,
                     "label": labels.get(c, ""),
                     "status": "labelled" if labels.get(c) else
                               ("blank label" if c in labels else "no dictionary entry")})
    for v in dict_vars:
        if v not in cols:
            rows.append({"variable": v, "in_data": False, "in_dictionary": True,
                         "label": labels[v], "status": "no such column"})
    return pd.DataFrame(rows)


def apply_labels(df: pd.DataFrame, dictionary: pd.DataFrame, *,
                 strict: bool = False) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Attach labels to ``df.attrs`` and return the frame with a coverage report.

    ``strict=True`` raises if any column is unlabelled or any dictionary entry
    has no column, for the final export where a gap is a defect.
    """
    cov = coverage(df, dictionary)
    if strict:
        bad = cov[cov["status"] != "labelled"]
        if not bad.empty:
            raise ValueError("apply_labels: unlabelled or unmatched variables:\n"
                             + bad[["variable", "status"]].to_string(index=False))
    labels = dict(zip(dictionary["variable"], dictionary["label"]))
    values = dict(zip(dictionary["variable"], dictionary["values"]))
    out = df.copy()
    out.attrs["variable_labels"] = {c: labels[c] for c in df.columns if labels.get(c)}
    out.attrs["value_labels"] = {c: values[c] for c in df.columns if values.get(c)}
    return out, cov


def write_labelled(df: pd.DataFrame, path, *, dictionary: pd.DataFrame | None = None) -> Path:
    """Write ``.dta`` or ``.sav`` with variable and value labels in the file.

    Uses the labels in ``df.attrs`` unless a dictionary is passed, in which case
    it is applied first. Stata variable names are limited to 32 characters and
    labels to 80; both are enforced here with an error rather than silently
    truncated by the writer.
    """
    import pyreadstat

    path = Path(path)
    if dictionary is not None:
        df, _ = apply_labels(df, dictionary)
    var_labels = df.attrs.get("variable_labels", {})
    val_labels = df.attrs.get("value_labels", {})

    if path.suffix.lower() == ".dta":
        too_long = [c for c in df.columns if len(str(c)) > 32]
        if too_long:
            raise ValueError(f"Stata variable names are limited to 32 characters: {too_long}")
        long_labels = {c: l for c, l in var_labels.items() if len(l) > 80}
        if long_labels:
            raise ValueError(f"Stata variable labels are limited to 80 characters: "
                             f"{list(long_labels)}")
        # Stata value labels attach to numeric variables only.
        numeric_val = {c: v for c, v in val_labels.items()
                       if pd.api.types.is_numeric_dtype(df[c])}
        pyreadstat.write_dta(df, str(path), column_labels=var_labels or None,
                             variable_value_labels=numeric_val or None)
    elif path.suffix.lower() == ".sav":
        pyreadstat.write_sav(df, str(path), column_labels=var_labels or None,
                             variable_value_labels=val_labels or None)
    else:
        raise ValueError(f"write_labelled: {path.suffix!r} cannot carry labels; "
                         "use .dta or .sav, or keep the dictionary CSV beside a CSV export")
    return path


def dictionary_from_file(path) -> pd.DataFrame:
    """Read a labelled ``.dta`` or ``.sav`` and emit a dictionary frame.

    The reverse direction: when the labelled file is what you were given and
    the dictionary is what you need to write down. Round-trips with
    `write_labelled`, which the tests check.
    """
    import pyreadstat

    path = Path(path)
    reader = {".dta": pyreadstat.read_dta, ".sav": pyreadstat.read_sav}.get(path.suffix.lower())
    if reader is None:
        raise ValueError(f"dictionary_from_file: cannot read labels from {path.suffix!r}")
    _, meta = reader(str(path), metadataonly=True)
    rows = []
    def tidy(code):
        # SPSS stores numeric codes as doubles, so 1 comes back as 1.0. Write
        # it as 1, so the dictionary round-trips through both formats identically.
        if isinstance(code, float) and code.is_integer():
            return int(code)
        return code

    for name, label in zip(meta.column_names, meta.column_labels):
        vals = meta.variable_value_labels.get(name, {})
        rows.append({"variable": name, "label": label or "",
                     "values": "|".join(f"{tidy(k)}={v}" for k, v in vals.items())})
    return pd.DataFrame(rows)
