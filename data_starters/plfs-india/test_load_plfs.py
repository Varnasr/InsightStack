"""
Tests for load_plfs.py, run against the synthetic fixtures rather than real
PLFS data.

    python make_fixture.py --outdir fixtures && python test_load_plfs.py

Each test corresponds to a way a PLFS analysis goes wrong without erroring.
"""

import os
import sys

import numpy as np
import pandas as pd

import load_plfs as L

FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
LAYOUT = os.path.join(FIX, "layout.csv")
HH = os.path.join(FIX, "CHHV1.txt")
PER = os.path.join(FIX, "CPerV1.txt")
failures = []


def check(name, condition, detail=""):
    if condition:
        print(f"  ok    {name}")
    else:
        print(f"  FAIL  {name}{': ' + detail if detail else ''}")
        failures.append(name)


def main():
    print("layout")
    layout = L.read_layout(LAYOUT)
    check("layout read", len(layout) > 0, f"{len(layout)} fields")
    check("end position derived", int(layout.loc[0, "end"]) ==
          int(layout.loc[0, "start"]) + int(layout.loc[0, "length"]) - 1)
    hh_layout = layout[layout["block"] == "household"]
    check("household block ends where the record ends",
          int(hh_layout["end"].max()) == 37, str(int(hh_layout["end"].max())))

    # An overlap means a shifted row, and everything after it reads wrong bytes.
    bad = layout.copy()
    bad.loc[bad["name"] == "State", "start"] = 2
    bad["end"] = bad["start"] + bad["length"] - 1
    try:
        L.validate_layout(bad)
        check("overlapping fields are rejected", False, "it accepted them")
    except L.PLFSError:
        check("overlapping fields are rejected", True)

    zero = layout.copy()
    zero.loc[zero["name"] == "State", "start"] = 0
    try:
        L.validate_layout(zero)
        check("a 0-indexed layout is rejected", False, "it accepted position 0")
    except L.PLFSError:
        check("a 0-indexed layout is rejected", True)

    print("fixed-width reading")
    hh = L.read_fixed_width(HH, layout, block="household", quiet=True)
    check("all household records read", len(hh) == 240, f"{len(hh)}")
    check("quarter is in range 1 to 4",
          bool(hh["Quarter"].between(1, 4).all()), str(sorted(hh["Quarter"].unique())))
    check("sector is 1 or 2", set(hh["Sector"].unique()) <= {1, 2},
          str(sorted(hh["Sector"].unique())))
    check("household size is plausible",
          bool(hh["Household_Size"].between(1, 8).all()),
          f"{hh['Household_Size'].min()}-{hh['Household_Size'].max()}")
    # A one-byte slip would put a digit of FSU_Serial_No into the household
    # number, or vice versa, and both would still parse as integers.
    check("FSU serial numbers are five digits",
          bool(hh["FSU_Serial_No"].between(10000, 99999).all()),
          f"{hh['FSU_Serial_No'].min()}-{hh['FSU_Serial_No'].max()}")

    print("implied decimals")
    check("MLTS divided by its two implied decimal places",
          1 < hh["MLTS"].mean() < 100000 and hh["MLTS"].mean() < 10000,
          f"mean {hh['MLTS'].mean():,.2f}")
    raw = L.read_fixed_width(HH, layout, block="household",
                             apply_decimals=False, quiet=True)
    check("the raw field is exactly 100 times the scaled one",
          bool(np.allclose(raw["MLTS"] / 100.0, hh["MLTS"])))
    check("integer fields are left alone",
          bool((raw["Household_Size"] == hh["Household_Size"]).all()))

    print("the weight rule")
    combined = L.apply_weight(hh, kind="combined", quiet=True)
    subsample = L.apply_weight(hh, kind="subsample", quiet=True)
    differ = combined["NSS"] != combined["NSC"]
    check("some second stage strata have NSS different from NSC",
          bool(differ.any()) and bool((~differ).any()),
          f"{int(differ.sum())} of {len(differ)}")
    check("MLTS/200 where NSS differs from NSC",
          bool(np.allclose(combined.loc[differ, "weight"],
                           combined.loc[differ, "MLTS"] / 200.0)))
    check("MLTS/100 where NSS equals NSC",
          bool(np.allclose(combined.loc[~differ, "weight"],
                           combined.loc[~differ, "MLTS"] / 100.0)))
    check("a sub-sample estimate always uses MLTS/100",
          bool(np.allclose(subsample["weight"], subsample["MLTS"] / 100.0)))
    # This is the whole point: dividing everything by 100 inflates the estimated
    # population, and nothing errors when you do it.
    naive_total = (hh["MLTS"] / 100.0 * hh["Household_Size"]).sum()
    correct_total = (combined["weight"] * combined["Household_Size"]).sum()
    check("the naive divide-by-100 inflates the population total",
          naive_total > correct_total * 1.2,
          f"{naive_total:,.0f} against {correct_total:,.0f}")

    no_nsc = hh.drop(columns=["NSC"])
    try:
        L.apply_weight(no_nsc, kind="combined", quiet=True)
        check("a combined weight without NSC is refused", False, "it computed one")
    except L.PLFSError:
        check("a combined weight without NSC is refused", True)

    print("keys")
    hh_keyed = L.build_key(combined, layout)
    widths = dict(zip(layout["name"], layout["length"]))
    expected_width = sum(int(widths[f]) for f in L.KEY_FIELDS)
    check("every key is the same length",
          set(hh_keyed["hhid"].str.len()) == {expected_width},
          str(sorted(set(hh_keyed["hhid"].str.len()))))
    check("keys are unique in the household file",
          not hh_keyed["hhid"].duplicated().any(),
          f"{int(hh_keyed['hhid'].duplicated().sum())} duplicates")
    # Without zero padding, FSU 1234 + household 5 and FSU 12345 + household
    # nothing collide. Concatenating the unpadded strings shows the collision.
    unpadded = (combined["FSU_Serial_No"].astype(int).astype(str)
                + combined["Sample_Household_No"].astype(int).astype(str))
    check("the padded key has at least as many distinct values as the unpadded one",
          hh_keyed["hhid"].nunique() >= unpadded.nunique())

    print("merging person to household")
    per = L.read_fixed_width(PER, layout, block="person", quiet=True)
    per_keyed = L.build_key(per, layout)
    merged = L.merge_person_household(per_keyed, hh_keyed, quiet=True)
    check("the merge does not change the person row count", len(merged) == len(per),
          f"{len(merged)} against {len(per)}")
    check("every person matched a household",
          not merged["Household_Size"].isna().any(),
          f"{int(merged['Household_Size'].isna().sum())} unmatched")

    # The strongest check available without real data: household size was
    # written into one file and the members into another, so they agree only if
    # the byte positions, the key padding and the merge are all correct.
    counted = merged.groupby("hhid").size()
    declared = hh_keyed.set_index("hhid")["Household_Size"]
    aligned = declared.reindex(counted.index)
    check("declared household size equals the number of person records",
          bool((counted == aligned).all()),
          f"{int((counted != aligned).sum())} households disagree")

    dupes = pd.concat([hh_keyed, hh_keyed.head(3)])
    try:
        L.merge_person_household(per_keyed, dupes, quiet=True)
        check("a duplicated household key is refused", False, "it merged anyway")
    except L.PLFSError:
        check("a duplicated household key is refused", True)

    print("record length")
    check("record length matches the layout",
          L.check_record_length(HH, layout[layout["block"] == "household"],
                                quiet=True) == 37)

    print()
    if failures:
        print(f"FAIL: {len(failures)} check(s) failed: {', '.join(failures)}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
