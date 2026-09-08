"""
Read PLFS unit-level data: fixed-width text, driven by the round's own layout.

PLFS arrives from MoSPI's microdata portal as plain text with no delimiters, no
header and no column names, plus a separate layout spreadsheet giving each
field's block, name, byte position and length. Nothing about the text file tells
you where a column starts. Everything here is therefore driven by the layout you
downloaded with your data, rather than by positions written into this script:
positions change between rounds, and a script that hardcodes them is a script
that quietly reads the wrong bytes a year later.

    from load_plfs import read_layout, read_fixed_width, apply_weight
    layout = read_layout("Data_LayoutPLFS_2022.csv")
    hh = read_fixed_width("CHHV1.txt", layout, block="household")
    hh = apply_weight(hh, kind="combined")

No data ships with this script. Register at microdata.gov.in and download the
round you want; see README.md.
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import pandas as pd

# Field names in the MoSPI README for PLFS January-December 2022. Names are
# stable across recent rounds; byte positions are not, which is why they are
# read from the layout rather than written here.
WEIGHT_FIELD = "MLTS"
SUBSAMPLE_FSU_FIELD = "NSS"
COMBINED_FSU_FIELD = "NSC"

# The common primary key, in the order MoSPI lists it. Lengths are taken from
# the layout at run time; these are the field names to look for.
KEY_FIELDS = ["Quarter", "FSU_Serial_No", "Hamlet_Group_Sub_Block_No",
              "Second_Stage_Stratum_No", "Sample_Household_No"]

LAYOUT_COLUMNS = ["block", "name", "start", "length", "decimals", "label"]


class PLFSError(Exception):
    """Raised when continuing would produce a wrong answer rather than no answer."""


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

def read_layout(path: str, sheet=0) -> pd.DataFrame:
    """Read a layout into the canonical form and check that it is usable.

    Accepts a CSV or an Excel export of MoSPI's Data_Layout file. Column names
    are matched loosely, because the header wording varies between rounds
    ("Byte Position", "Start", "Position (From)" have all appeared).

    Positions in MoSPI layouts are 1-indexed and inclusive, which is the single
    most common source of a silently misread file: Python slices from 0, so a
    field at position 32 of length 5 is characters [31:36], not [32:37]. Reading
    one byte late produces numbers rather than an error.
    """
    if path.lower().endswith((".xlsx", ".xls")):
        raw = pd.read_excel(path, sheet_name=sheet)
    else:
        raw = pd.read_csv(path)

    rename = {}
    for col in raw.columns:
        key = str(col).strip().lower().replace("_", " ")
        if key in ("block", "block no", "block number", "schedule block"):
            rename[col] = "block"
        elif key in ("name", "field name", "column name", "variable", "variable name"):
            rename[col] = "name"
        elif key in ("start", "byte position", "position from", "from", "start position"):
            rename[col] = "start"
        elif key in ("length", "size", "bytes", "field length"):
            rename[col] = "length"
        elif key in ("decimals", "decimal", "no of decimals", "decimal places"):
            rename[col] = "decimals"
        elif key in ("label", "description", "field description"):
            rename[col] = "label"
    layout = raw.rename(columns=rename)

    missing = [c for c in ("name", "start", "length") if c not in layout.columns]
    if missing:
        raise PLFSError(
            f"The layout is missing {', '.join(missing)}. Expected columns like "
            f"{LAYOUT_COLUMNS}. Rename the columns of your MoSPI layout export to match."
        )
    for col in ("block", "decimals", "label"):
        if col not in layout.columns:
            layout[col] = 0 if col == "decimals" else ""

    layout = layout[LAYOUT_COLUMNS].copy()
    layout["name"] = layout["name"].astype(str).str.strip()
    for col in ("start", "length", "decimals"):
        layout[col] = pd.to_numeric(layout[col], errors="coerce")
    layout["decimals"] = layout["decimals"].fillna(0)
    layout = layout.dropna(subset=["start", "length"])
    layout[["start", "length", "decimals"]] = layout[["start", "length", "decimals"]].astype(int)
    layout["end"] = layout["start"] + layout["length"] - 1

    validate_layout(layout)
    return layout.reset_index(drop=True)


def validate_layout(layout: pd.DataFrame) -> list[str]:
    """Refuse a layout that cannot describe a real file, and report the odd bits.

    Overlapping fields are fatal: two columns cannot occupy one byte, and the
    usual cause is a transcription slip that shifts everything after it. Gaps
    are not fatal, because MoSPI layouts do legitimately leave filler bytes, but
    they are worth seeing.
    """
    problems = []
    if (layout["start"] < 1).any():
        bad = layout.loc[layout["start"] < 1, "name"].tolist()
        raise PLFSError(f"Positions must be 1-indexed; these start below 1: {bad}")
    if (layout["length"] < 1).any():
        bad = layout.loc[layout["length"] < 1, "name"].tolist()
        raise PLFSError(f"These fields have a length below 1: {bad}")

    for block, chunk in layout.groupby(layout["block"].astype(str), sort=False):
        chunk = chunk.sort_values("start")
        prev_end, prev_name = 0, None
        for row in chunk.itertuples():
            if row.start <= prev_end:
                raise PLFSError(
                    f"In block {block!r}, {row.name} starts at byte {row.start} but "
                    f"{prev_name} already runs to byte {prev_end}. Overlapping fields "
                    "usually mean a shifted row in the layout, and every field after "
                    "it will read the wrong bytes."
                )
            if row.start > prev_end + 1 and prev_name is not None:
                problems.append(f"block {block}: bytes {prev_end + 1}-{row.start - 1} "
                                f"unused between {prev_name} and {row.name}")
            prev_end, prev_name = row.end, row.name
    return problems


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

def read_fixed_width(path: str, layout: pd.DataFrame, block=None, columns=None,
                     apply_decimals: bool = True, quiet: bool = False) -> pd.DataFrame:
    """Read a PLFS text file using the layout.

    `block` selects one block of the schedule; `columns` selects field names.
    Reading only what you need matters: the person file for a single year runs
    to several hundred thousand records.
    """
    spec = layout
    if block is not None:
        spec = spec[spec["block"].astype(str) == str(block)]
        if spec.empty:
            available = sorted(layout["block"].astype(str).unique())
            raise PLFSError(f"No block {block!r} in the layout. Available: {available}")
    if columns is not None:
        wanted = list(columns)
        present = set(spec["name"])
        absent = [c for c in wanted if c not in present]
        if absent and not quiet:
            print(f"  not in this layout: {', '.join(absent)}", file=sys.stderr)
        spec = spec[spec["name"].isin(wanted)]
        if spec.empty:
            raise PLFSError("None of the requested fields exist in this layout.")

    spec = spec.sort_values("start")
    # MoSPI positions are 1-indexed and inclusive; pandas colspecs are 0-indexed
    # and half-open. This conversion is the whole ball game.
    colspecs = [(int(r.start) - 1, int(r.start) - 1 + int(r.length)) for r in spec.itertuples()]
    names = spec["name"].tolist()

    df = pd.read_fwf(path, colspecs=colspecs, names=names, dtype=str, header=None)
    check_record_length(path, layout, quiet=quiet)

    for col in names:
        df[col] = pd.to_numeric(df[col].str.strip(), errors="coerce")

    if apply_decimals:
        df = apply_implied_decimals(df, spec, quiet=quiet)
    if not quiet:
        print(f"  {len(df):,} records, {len(names)} fields", file=sys.stderr)
    return df


def apply_implied_decimals(df: pd.DataFrame, spec: pd.DataFrame,
                           quiet: bool = False) -> pd.DataFrame:
    """Divide each field by ten to the power of its declared decimal places.

    PLFS stores decimals implicitly: MLTS is ten bytes holding a number with two
    implied decimal places, so the characters 0000123456 mean 1234.56. The scale
    comes from the layout rather than from anything in this script, so it stays
    right when a round changes it.
    """
    df = df.copy()
    for row in spec.itertuples():
        if row.decimals and row.name in df.columns:
            df[row.name] = df[row.name] / (10 ** int(row.decimals))
            if not quiet:
                print(f"  {row.name}: {row.decimals} implied decimal place(s)", file=sys.stderr)
    return df


def check_record_length(path: str, layout: pd.DataFrame, quiet: bool = False) -> int:
    """Compare the file's line length against the last byte the layout describes."""
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        first = fh.readline().rstrip("\n").rstrip("\r")
    actual, declared = len(first), int(layout["end"].max())
    if actual != declared and not quiet:
        print(f"  record length is {actual} but the layout describes {declared} bytes. "
              "Check that the layout and the data are from the same round.",
              file=sys.stderr)
    return actual


# ---------------------------------------------------------------------------
# Weights
# ---------------------------------------------------------------------------

def apply_weight(df: pd.DataFrame, kind: str = "combined", weight_field: str = WEIGHT_FIELD,
                 quiet: bool = False) -> pd.DataFrame:
    """Add the final weight, following MoSPI's rule rather than dividing by 100.

    From the README shipped with the data:

        For generating sub-sample wise estimate for the Calendar Year, weight
        may be applied as follows:
             Final Weight = MLTS/100
        For generating combined estimate for the Calendar Year (taking both the
        subsamples together), weights may be applied as follows:
             Final weight = MLTS/100   if NSS=NSC
                          = MLTS/200   otherwise.

    NSS is the number of first stage units surveyed in the sub-sample within a
    second stage stratum; NSC is the same count for both sub-samples combined.
    Where they differ, both sub-samples are present and each carries half the
    weight. Dividing everything by 100 therefore doubles the estimated
    population exactly where the sub-samples differ, and does so silently: the
    ratios and rates barely move, so a labour force participation rate looks
    fine while every employment total is wrong.
    """
    if kind not in ("combined", "subsample"):
        raise PLFSError("kind must be 'combined' or 'subsample'")
    if weight_field not in df.columns:
        raise PLFSError(
            f"{weight_field} is not in the DataFrame, so no weighted estimate is "
            "possible. Include it in the fields you read."
        )

    df = df.copy()
    mlts = pd.to_numeric(df[weight_field], errors="coerce")

    if kind == "subsample":
        df["weight"] = mlts / 100.0
        if not quiet:
            print("  sub-sample weight: MLTS/100", file=sys.stderr)
        return df

    for field in (SUBSAMPLE_FSU_FIELD, COMBINED_FSU_FIELD):
        if field not in df.columns:
            raise PLFSError(
                f"A combined estimate needs {SUBSAMPLE_FSU_FIELD} and "
                f"{COMBINED_FSU_FIELD} to decide between MLTS/100 and MLTS/200, and "
                f"{field} is missing. Read it in, or pass kind='subsample' if that "
                "is really what you want."
            )
    nss = pd.to_numeric(df[SUBSAMPLE_FSU_FIELD], errors="coerce")
    nsc = pd.to_numeric(df[COMBINED_FSU_FIELD], errors="coerce")
    halved = nss.ne(nsc)
    df["weight"] = np.where(halved, mlts / 200.0, mlts / 100.0)
    if not quiet:
        print(f"  combined weight: MLTS/100 for {int((~halved).sum()):,} records, "
              f"MLTS/200 for {int(halved.sum()):,} where NSS differs from NSC",
              file=sys.stderr)
    return df


# ---------------------------------------------------------------------------
# Keys and merging
# ---------------------------------------------------------------------------

def build_key(df: pd.DataFrame, layout: pd.DataFrame, fields=None,
              name: str = "hhid") -> pd.DataFrame:
    """Build the household key by zero-padding each part to its layout length.

    MoSPI's common primary key is Quarter, FSU serial number, hamlet group or
    sub-block, second stage stratum and sample household number. Concatenating
    them without padding to the declared field width collapses distinct
    households onto one key: FSU 1234 with household 5 and FSU 12345 with
    household nothing both read as "12345". The merge then succeeds and is wrong.
    """
    fields = list(fields or KEY_FIELDS)
    widths = dict(zip(layout["name"], layout["length"]))
    missing = [f for f in fields if f not in df.columns]
    if missing:
        raise PLFSError(f"Key fields absent from the data: {missing}")

    parts = []
    for field in fields:
        width = int(widths.get(field, 0))
        if width < 1:
            raise PLFSError(f"No length for key field {field!r} in the layout.")
        parts.append(df[field].fillna(-1).astype("int64").astype(str).str.zfill(width))
    out = df.copy()
    out[name] = parts[0]
    for part in parts[1:]:
        out[name] = out[name] + part
    return out


def merge_person_household(person: pd.DataFrame, household: pd.DataFrame,
                           on: str = "hhid", quiet: bool = False) -> pd.DataFrame:
    """Attach household fields to person records, and refuse a merge that inflates.

    A many-to-many merge on a key that is not unique in the household file
    multiplies rows and inflates every weighted total. This checks first.
    """
    dupes = int(household[on].duplicated().sum())
    if dupes:
        raise PLFSError(
            f"{dupes:,} duplicated {on} values in the household file, so the merge "
            "would multiply person records. Check the key fields and the visit or "
            "quarter selection before merging."
        )
    before = len(person)
    merged = person.merge(household, on=on, how="left", suffixes=("", "_hh"))
    if len(merged) != before:
        raise PLFSError(f"The merge changed the row count from {before:,} to {len(merged):,}.")
    unmatched = int(merged[household.columns.difference([on])[0]].isna().sum()) \
        if len(household.columns) > 1 else 0
    if unmatched and not quiet:
        print(f"  {unmatched:,} of {before:,} person records matched no household",
              file=sys.stderr)
    return merged


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("layout", help="MoSPI Data_Layout file (.csv or .xlsx)")
    p.add_argument("data", help="PLFS fixed-width text file, e.g. CHHV1.txt")
    p.add_argument("--block", default=None, help="Block of the schedule to read")
    p.add_argument("--fields", nargs="*", default=None, help="Field names to read")
    p.add_argument("--weight", choices=["combined", "subsample", "none"], default="combined")
    p.add_argument("--out", default=None, help="Write the result to this CSV")
    a = p.parse_args(argv)

    try:
        layout = read_layout(a.layout)
        print(f"  layout: {len(layout)} fields, {layout['end'].max()} bytes", file=sys.stderr)
        df = read_fixed_width(a.data, layout, block=a.block, columns=a.fields)
        if a.weight != "none":
            df = apply_weight(df, kind=a.weight)
    except PLFSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if "weight" in df.columns:
        print(f"  sum of weights: {df['weight'].sum():,.0f}", file=sys.stderr)
    if a.out:
        df.to_csv(a.out, index=False)
        print(f"  written to {a.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
