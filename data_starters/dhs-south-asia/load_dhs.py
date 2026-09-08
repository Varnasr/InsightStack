"""
Load a DHS recode file without running out of memory, attach the survey design,
and refuse to continue quietly when something is wrong.

Covers every DHS survey in South Asia (see surveys.csv). The recode structure is
the same in all of them, so one loader serves India, Bangladesh, Nepal, Pakistan,
Maldives, Afghanistan and Sri Lanka.

Requires: pandas, and pyreadstat if you want column selection on .DTA/.SAV
(strongly recommended: NFHS-5's individual recode is 724,115 rows by roughly
5,000 columns, and reading all of it is what makes laptops swap).

    python load_dhs.py IAIR7EFL.DTA --vars v012 v106 v190 v201 --out nfhs5_women.csv

Or as a library:

    from load_dhs import read_recode
    df = read_recode("IAIR7EFL.DTA", ["v012", "v106", "v190"])

No data ships with this script. You download the files yourself from
dhsprogram.com after your data request is approved; see README.md.
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from dataclasses import dataclass

import pandas as pd

try:
    import pyreadstat

    HAVE_PYREADSTAT = True
except ImportError:  # pragma: no cover - depends on the environment
    HAVE_PYREADSTAT = False


HERE = os.path.dirname(os.path.abspath(__file__))
VARIABLES_CSV = os.path.join(HERE, "variables.csv")

# Weight, PSU and strata differ by recode type. Getting this wrong does not
# error; it silently produces standard errors for the wrong design.
DESIGN = {
    "IR": {"weight": "v005", "psu": "v021", "strata": "v022", "strata_alt": "v023"},
    "KR": {"weight": "v005", "psu": "v021", "strata": "v022", "strata_alt": "v023"},
    "BR": {"weight": "v005", "psu": "v021", "strata": "v022", "strata_alt": "v023"},
    "CR": {"weight": "v005", "psu": "v021", "strata": "v022", "strata_alt": "v023"},
    "MR": {"weight": "mv005", "psu": "mv021", "strata": "mv022", "strata_alt": "mv023"},
    "HR": {"weight": "hv005", "psu": "hv021", "strata": "hv022", "strata_alt": "hv023"},
    "PR": {"weight": "hv005", "psu": "hv021", "strata": "hv022", "strata_alt": "hv023"},
}

RECODE_NAMES = {
    "IR": "Individual Recode (women 15-49)",
    "MR": "Men's Recode",
    "KR": "Children's Recode (births in the last 5 years, living or dead)",
    "BR": "Births Recode (full birth history)",
    "HR": "Household Recode",
    "PR": "Household Member Recode",
    "CR": "Couples Recode",
}

# WHO 2006 plausibility bounds. DHS stores these z-scores multiplied by 100 and
# uses values at or above 9990 for flags and missing.
ANTHRO_BOUNDS = {"haz": (-6, 6), "waz": (-6, 5), "whz": (-5, 5), "bmiz": (-5, 5)}
ANTHRO_COLS = {"haz": ("hw70", "hc70"), "waz": ("hw71", "hc71"),
               "whz": ("hw72", "hc72"), "bmiz": ("hw73", "hc73")}

FILENAME_RE = re.compile(
    # The two characters after the recode are the phase number and then a
    # version character that is incremented when DHS reissues the file. That
    # version can be a digit: NFHS-4's individual recode is IAIR74FL.DTA.
    r"^(?P<country>[A-Z]{2})(?P<recode>IR|MR|KR|BR|HR|PR|CR|GE|HW)"
    r"(?P<phase>[0-9A-Z])(?P<release>[0-9A-Z])(?P<fmt>FL|DT|SV|SD)",
    re.IGNORECASE,
)


@dataclass
class DHSFile:
    country: str
    recode: str
    phase: str
    release: str
    fmt: str
    path: str

    def describe(self) -> str:
        return (f"{os.path.basename(self.path)}: country {self.country}, "
                f"{self.recode} = {RECODE_NAMES.get(self.recode, 'unknown recode')}, "
                f"phase {self.phase}, release {self.release}")


class DHSError(Exception):
    """Raised when continuing would produce a wrong answer rather than no answer."""


def parse_filename(path: str) -> DHSFile:
    """Read country, recode type and phase out of a DHS filename.

    DHS names files {CC}{RR}{phase}{release}{format}, so IAIR7EFL.DTA is India,
    Individual Recode, phase 7, release E, flat. Renaming the file breaks this,
    which is why every function here lets you pass `recode` explicitly.
    """
    stem = os.path.basename(path)
    m = FILENAME_RE.match(stem)
    if not m:
        raise DHSError(
            f"Cannot read a DHS filename out of {stem!r}. Expected something like "
            "IAIR7EFL.DTA. If you renamed the file, pass recode= explicitly."
        )
    g = m.groupdict()
    return DHSFile(country=g["country"].upper(), recode=g["recode"].upper(),
                   phase=g["phase"].upper(), release=g["release"].upper(),
                   fmt=g["fmt"].upper(), path=path)


def load_variable_table(csv_path: str = VARIABLES_CSV) -> list[dict]:
    with open(csv_path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def scale_factors(recode: str, csv_path: str = VARIABLES_CSV) -> dict[str, float]:
    """Map every variable that needs rescaling to its divisor, for this recode.

    Reads variables.csv so the documented scale and the applied scale cannot
    drift apart.
    """
    column = {"MR": "mr_var"}.get(recode, "hr_pr_var" if recode in ("HR", "PR") else "ir_kr_br_var")
    out: dict[str, float] = {}
    for row in load_variable_table(csv_path):
        var = (row.get(column) or "").strip()
        scale = (row.get("scale") or "").strip().lower()
        if not var or not scale.startswith("divide by"):
            continue
        try:
            out[var] = float(scale.split("divide by")[1].strip())
        except (IndexError, ValueError):
            continue
    return out


def available_columns(path: str) -> list[str]:
    """Column names without reading a single row of data."""
    if not HAVE_PYREADSTAT:
        raise DHSError("Reading metadata alone needs pyreadstat: pip install pyreadstat")
    reader = pyreadstat.read_dta if path.lower().endswith(".dta") else pyreadstat.read_sav
    _, meta = reader(path, metadataonly=True)
    return list(meta.column_names)


def read_recode(path: str, variables=None, recode: str | None = None,
                add_design: bool = True, apply_scales: bool = True,
                quiet: bool = False) -> pd.DataFrame:
    """Read selected variables from a DHS recode file.

    `variables` is the analysis variables you want. The design variables for the
    recode are added automatically, so you never have to remember that the men's
    recode weights on mv005 rather than v005.

    Variables absent from this round are reported rather than silently dropped.
    That report is the cross-round harmonisation problem made visible: v190 is
    missing from pre-2000 rounds, and sdist exists only for India from NFHS-4 on.
    """
    info = parse_filename(path) if recode is None else None
    recode = (recode or info.recode).upper()
    if recode not in DESIGN:
        raise DHSError(f"No design defined for recode {recode!r}. Known: {sorted(DESIGN)}")

    design = DESIGN[recode]
    wanted: list[str] | None = None
    if variables is not None:
        wanted = list(dict.fromkeys(list(variables) + [design["weight"], design["psu"],
                                                       design["strata"], design["strata_alt"]]))

    if wanted is not None and HAVE_PYREADSTAT:
        present = set(available_columns(path))
        missing = [v for v in wanted if v not in present]
        usecols = [v for v in wanted if v in present]
        if missing and not quiet:
            print(f"  not in this file: {', '.join(missing)}", file=sys.stderr)
        if not usecols:
            raise DHSError("None of the requested variables exist in this file.")
        reader = pyreadstat.read_dta if path.lower().endswith(".dta") else pyreadstat.read_sav
        df, _ = reader(path, usecols=usecols)
    else:
        if wanted is not None and not quiet:
            print("  pyreadstat not installed, reading the whole file "
                  "(slow and memory hungry on large surveys)", file=sys.stderr)
        df = (pd.read_stata(path, convert_categoricals=False)
              if path.lower().endswith(".dta") else pd.read_spss(path, convert_categoricals=False))
        if wanted is not None:
            df = df[[c for c in wanted if c in df.columns]]

    if apply_scales:
        df = rescale(df, recode, quiet=quiet)
    if add_design:
        df = attach_design(df, recode, quiet=quiet)
    return df


# Columns that must not be rescaled here, because something else owns them.
# Weights belong to attach_design, which needs the raw value to tell a genuine
# DHS weight from one that has already been divided. Anthropometry belongs to
# clean_anthropometry, which has to spot the flags at 9990 and above *before*
# anything divides them down into the plausible range.
_OWNED_ELSEWHERE = ({d["weight"] for d in DESIGN.values()}
                    | {col for pair in ANTHRO_COLS.values() for col in pair})


def rescale(df: pd.DataFrame, recode: str, quiet: bool = False) -> pd.DataFrame:
    """Divide the variables DHS stores as integers by their documented factor."""
    df = df.copy()
    for var, factor in scale_factors(recode).items():
        if var in df.columns and var not in _OWNED_ELSEWHERE:
            df[var] = pd.to_numeric(df[var], errors="coerce") / factor
            if not quiet:
                print(f"  scaled {var} by 1/{factor:g}", file=sys.stderr)
    return df


def attach_design(df: pd.DataFrame, recode: str, quiet: bool = False) -> pd.DataFrame:
    """Add weight, psu and strata columns, and complain when the design is broken."""
    design = DESIGN[recode.upper()]
    df = df.copy()

    wcol = design["weight"]
    if wcol not in df.columns:
        raise DHSError(
            f"{wcol} is missing, so nothing weighted can be computed from this file. "
            "Include it in your variable list."
        )
    raw = pd.to_numeric(df[wcol], errors="coerce")
    if raw.dropna().empty:
        raise DHSError(f"{wcol} is entirely missing.")
    mean_raw = raw.mean()
    if mean_raw < 1000:
        raise DHSError(
            f"{wcol} averages {mean_raw:,.2f}, which is far below the ~1,000,000 a raw "
            "DHS weight should average. This file looks pre-scaled or is not a DHS "
            "recode. Dividing again would shrink every weighted total by a million."
        )
    df["weight"] = raw / 1_000_000

    if design["psu"] in df.columns:
        df["psu"] = df[design["psu"]]
    strata_col = next((c for c in (design["strata"], design["strata_alt"]) if c in df.columns), None)
    if strata_col:
        df["strata"] = df[strata_col]
        if not quiet and strata_col == design["strata_alt"]:
            print(f"  design strata taken from {strata_col} "
                  f"({design['strata']} absent, normal in older rounds)", file=sys.stderr)
    elif not quiet:
        print("  no strata variable found; variance estimates will be wrong "
              "unless the design really is unstratified", file=sys.stderr)
    return df


def clean_anthropometry(df: pd.DataFrame, recode: str = "KR", quiet: bool = False) -> pd.DataFrame:
    """Turn DHS anthropometry into usable z-scores.

    Three things go wrong here and none of them raise an error on their own:
    the values are stored times 100, flags and missing sit at 9990 and above,
    and the columns are hw70-hw73 in the children's recode but hc70-hc73 in the
    household member recode.
    """
    idx = 1 if recode.upper() == "PR" else 0
    df = df.copy()
    for name, cols in ANTHRO_COLS.items():
        col = cols[idx]
        if col not in df.columns:
            continue
        raw = pd.to_numeric(df[col], errors="coerce")
        flagged = int((raw >= 9990).sum())
        z = raw.where(raw < 9990) / 100.0
        lo, hi = ANTHRO_BOUNDS[name]
        out_of_range = int(((z < lo) | (z > hi)).sum())
        df[name] = z.where((z >= lo) & (z <= hi))
        if not quiet:
            print(f"  {name} from {col}: {flagged:,} flagged or missing, "
                  f"{out_of_range:,} outside WHO bounds [{lo}, {hi}]", file=sys.stderr)
    return df


def cmc_to_year_month(cmc):
    """Century month code to (year, month). CMC 1441 is January 2020."""
    cmc = pd.to_numeric(cmc, errors="coerce")
    year = 1900 + ((cmc - 1) // 12)
    month = cmc - 12 * (year - 1900)
    return year, month


def year_month_to_cmc(year, month):
    return (year - 1900) * 12 + month


def summarise(df: pd.DataFrame, recode: str) -> str:
    lines = [f"rows: {len(df):,}", f"columns: {len(df.columns)}"]
    if "weight" in df.columns:
        lines.append(f"sum of weights: {df['weight'].sum():,.0f} "
                     f"(should be close to the unweighted row count)")
    if "psu" in df.columns:
        lines.append(f"clusters: {df['psu'].nunique():,}")
    if "strata" in df.columns:
        singles = df.groupby("strata")["psu"].nunique().eq(1).sum() if "psu" in df.columns else 0
        lines.append(f"strata: {df['strata'].nunique():,}"
                     + (f", of which {singles} contain a single cluster" if singles else ""))
    return "\n".join("  " + line for line in lines)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("path", help="Path to a DHS recode file (.DTA or .SAV)")
    p.add_argument("--vars", nargs="*", default=None,
                   help="Analysis variables. Design variables are added for you. "
                        "Omit to read every column, which you probably do not want.")
    p.add_argument("--recode", default=None, help="Override the recode type (IR, MR, KR, ...)")
    p.add_argument("--anthro", action="store_true", help="Clean hw70-hw73 or hc70-hc73 into z-scores")
    p.add_argument("--out", default=None, help="Write the result to this CSV")
    a = p.parse_args(argv)

    try:
        info = parse_filename(a.path)
        print(info.describe(), file=sys.stderr)
    except DHSError as exc:
        if a.recode is None:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        info = None

    recode = (a.recode or info.recode).upper()
    try:
        df = read_recode(a.path, a.vars, recode=recode)
        if a.anthro:
            df = clean_anthropometry(df, recode)
    except DHSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(summarise(df, recode), file=sys.stderr)
    if a.out:
        df.to_csv(a.out, index=False)
        print(f"  written to {a.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
