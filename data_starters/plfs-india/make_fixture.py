"""
Build a small synthetic PLFS-shaped fixture: a layout file and two fixed-width
text files, one household and one person.

MoSPI's terms do not allow the unit-level data to be passed on, and the real
files run to hundreds of thousands of records besides. These fixtures carry the
structure that matters and nothing else: 1-indexed inclusive byte positions,
implied decimal places on the multiplier, NSS and NSC that agree for some second
stage strata and differ for others, and a five-part household key whose parts
need zero padding. Every value comes from a seeded generator and none of it is
data about anybody.

    python make_fixture.py --outdir fixtures
"""

from __future__ import annotations

import argparse
import csv
import os

import numpy as np

SEED = 20260908

# (block, name, length, decimals, label). Positions are derived, so the fixture
# cannot drift out of step with itself.
HOUSEHOLD_FIELDS = [
    ("household", "Quarter", 2, 0, "Quarter of the calendar year"),
    ("household", "State", 2, 0, "State code"),
    ("household", "Sector", 1, 0, "1 rural, 2 urban"),
    ("household", "Stratum", 2, 0, "Stratum"),
    ("household", "Sub_Stratum", 2, 0, "Sub-stratum, rural only"),
    ("household", "Sub_Sample", 1, 0, "Sub-sample code"),
    ("household", "FSU_Serial_No", 5, 0, "First stage unit serial number"),
    ("household", "Hamlet_Group_Sub_Block_No", 1, 0, "Hamlet group or sub-block"),
    ("household", "Second_Stage_Stratum_No", 1, 0, "Second stage stratum"),
    ("household", "Sample_Household_No", 2, 0, "Sample household number"),
    ("household", "Household_Size", 2, 0, "Number of members"),
    ("household", "NSS", 3, 0, "FSUs surveyed in the sub-sample within the SSS"),
    ("household", "NSC", 3, 0, "FSUs surveyed in combined sub-samples within the SSS"),
    ("household", "MLTS", 10, 2, "Multiplier at second stage stratum level"),
]

PERSON_FIELDS = [
    ("person", "Quarter", 2, 0, "Quarter of the calendar year"),
    ("person", "FSU_Serial_No", 5, 0, "First stage unit serial number"),
    ("person", "Hamlet_Group_Sub_Block_No", 1, 0, "Hamlet group or sub-block"),
    ("person", "Second_Stage_Stratum_No", 1, 0, "Second stage stratum"),
    ("person", "Sample_Household_No", 2, 0, "Sample household number"),
    ("person", "Person_Serial_No", 2, 0, "Person serial number in the household"),
    ("person", "Age", 3, 0, "Age in completed years"),
    ("person", "Sex", 1, 0, "1 male, 2 female, 3 transgender"),
    ("person", "Education", 2, 0, "General education level"),
    ("person", "Status_Code_UPS", 2, 0, "Usual principal status activity code"),
]


def _layout_rows():
    rows, pos = [], {}
    for block, fields in (("household", HOUSEHOLD_FIELDS), ("person", PERSON_FIELDS)):
        start = 1
        for blk, name, length, decimals, label in fields:
            rows.append({"block": blk, "name": name, "start": start,
                         "length": length, "decimals": decimals, "label": label})
            start += length
        pos[block] = start - 1
    return rows, pos


def _fmt(value: int, width: int) -> str:
    text = str(int(value))
    if len(text) > width:
        raise ValueError(f"{value} does not fit in {width} bytes")
    return text.zfill(width)


def build(outdir: str) -> list[str]:
    os.makedirs(outdir, exist_ok=True)
    rng = np.random.default_rng(SEED)
    rows, _ = _layout_rows()

    layout_path = os.path.join(outdir, "layout.csv")
    with open(layout_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["block", "name", "start", "length",
                                           "decimals", "label"])
        w.writeheader()
        w.writerows(rows)

    n_fsu, hh_per_fsu = 60, 4
    households, people = [], []
    for f in range(n_fsu):
        fsu = 10000 + f * 7
        sector = 1 if f % 2 == 0 else 2
        sss = (f % 3) + 1
        # In half the second stage strata both sub-samples are present, so
        # NSS differs from NSC and the combined weight is MLTS/200.
        nsc = 8 if f % 2 == 0 else 4
        nss = 4 if f % 2 == 0 else 4
        for h in range(hh_per_fsu):
            size = int(rng.integers(1, 9))
            households.append({
                "Quarter": (f % 4) + 1, "State": int(rng.integers(1, 36)),
                "Sector": sector, "Stratum": int(rng.integers(1, 7)),
                "Sub_Stratum": int(rng.integers(1, 9)) if sector == 1 else 0,
                "Sub_Sample": (f % 2) + 1, "FSU_Serial_No": fsu,
                "Hamlet_Group_Sub_Block_No": 0, "Second_Stage_Stratum_No": sss,
                "Sample_Household_No": h + 1, "Household_Size": size,
                "NSS": nss, "NSC": nsc,
                # Stored with two implied decimal places.
                "MLTS": int(rng.normal(120000, 25000)),
            })
            for m in range(size):
                people.append({
                    "Quarter": (f % 4) + 1, "FSU_Serial_No": fsu,
                    "Hamlet_Group_Sub_Block_No": 0, "Second_Stage_Stratum_No": sss,
                    "Sample_Household_No": h + 1, "Person_Serial_No": m + 1,
                    "Age": int(rng.integers(0, 90)), "Sex": int(rng.integers(1, 3)),
                    "Education": int(rng.integers(1, 13)),
                    "Status_Code_UPS": int(rng.choice([11, 21, 31, 41, 51, 81, 91, 92])),
                })

    written = [layout_path]
    for block, records, fields in (("household", households, HOUSEHOLD_FIELDS),
                                   ("person", people, PERSON_FIELDS)):
        path = os.path.join(outdir, f"C{'HH' if block == 'household' else 'Per'}V1.txt")
        with open(path, "w") as fh:
            for rec in records:
                fh.write("".join(_fmt(rec[name], length)
                                 for _b, name, length, _d, _l in fields) + "\n")
        written.append(path)
    return written


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--outdir", default="fixtures")
    for path in build(p.parse_args().outdir):
        print(f"wrote {path}")
