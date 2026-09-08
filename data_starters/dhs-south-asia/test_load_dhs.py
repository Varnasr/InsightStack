"""
Tests for load_dhs.py, run against the synthetic fixtures rather than real DHS data.

    python make_fixture.py --outdir fixtures && python test_load_dhs.py

Each test corresponds to a way a DHS analysis goes wrong without erroring.
"""

import os
import sys

import numpy as np
import pandas as pd

import load_dhs as L

FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
failures = []


def check(name, condition, detail=""):
    if condition:
        print(f"  ok    {name}")
    else:
        print(f"  FAIL  {name}{': ' + detail if detail else ''}")
        failures.append(name)


def main():
    print("filename parsing")
    f = L.parse_filename(os.path.join(FIX, "XXIR7AFL.DTA"))
    check("recode read from filename", f.recode == "IR", f.recode)
    check("phase read from filename", f.phase == "7", f.phase)
    try:
        L.parse_filename("women_final.dta")
        check("a renamed file is rejected", False)
    except L.DHSError:
        check("a renamed file is rejected", True)
    # The version character after the phase can be a digit, not only a letter.
    check("NFHS-4 style IAIR74FL parses",
          L.parse_filename("IAIR74FL.DTA").recode == "IR")
    check("NFHS-5 style IAIR7EFL parses",
          L.parse_filename("IAIR7EFL.DTA").recode == "IR")
    check("Bangladesh BDKR81FL parses",
          L.parse_filename("BDKR81FL.DTA").recode == "KR")
    check("country code read correctly",
          L.parse_filename("NPIR82FL.DTA").country == "NP")

    print("weights")
    ir = L.read_recode(os.path.join(FIX, "XXIR7AFL.DTA"), ["v012", "v106", "v190"], quiet=True)
    check("weight column added", "weight" in ir.columns)
    check("weight divided by a million", abs(ir["weight"].mean() - 1) < 0.1,
          f"mean {ir['weight'].mean():.4f}")
    check("sum of weights near the row count",
          abs(ir["weight"].sum() - len(ir)) / len(ir) < 0.05,
          f"{ir['weight'].sum():,.0f} vs {len(ir):,}")

    # Feeding back an already-scaled file must be refused, not silently divided again.
    scaled = pd.read_stata(os.path.join(FIX, "XXIR7AFL.DTA"), convert_categoricals=False)
    scaled["v005"] = scaled["v005"] / 1_000_000
    tmp = os.path.join(FIX, "_prescaled.dta")
    scaled.to_stata(tmp, write_index=False)
    try:
        L.read_recode(tmp, ["v012"], recode="IR", quiet=True)
        check("pre-scaled weights are refused", False, "it accepted them")
    except L.DHSError:
        check("pre-scaled weights are refused", True)
    finally:
        os.remove(tmp)

    print("design")
    check("psu attached", "psu" in ir.columns)
    check("strata attached", "strata" in ir.columns)
    mr = L.read_recode(os.path.join(FIX, "XXMR7AFL.DTA"), ["mv012"], quiet=True)
    check("men's recode weights on mv005", abs(mr["weight"].mean() - 1) < 0.1,
          f"mean {mr['weight'].mean():.4f}")
    hr = L.read_recode(os.path.join(FIX, "XXHR7AFL.DTA"), ["hv270"], quiet=True)
    check("household recode weights on hv005", abs(hr["weight"].mean() - 1) < 0.1,
          f"mean {hr['weight'].mean():.4f}")

    print("scale factors from variables.csv")
    ir2 = L.read_recode(os.path.join(FIX, "XXIR7AFL.DTA"), ["v437", "v438", "v191"], quiet=True)
    check("woman's weight in kg not decikg", 30 < ir2["v437"].mean() < 90,
          f"mean {ir2['v437'].mean():.1f}")
    check("woman's height in cm", 140 < ir2["v438"].mean() < 165,
          f"mean {ir2['v438'].mean():.1f}")
    check("wealth score divided by 100,000", abs(ir2["v191"].mean()) < 5,
          f"mean {ir2['v191'].mean():.3f}")
    check("v005 not double-scaled by the scale table",
          abs(ir2["weight"].mean() - 1) < 0.1)

    print("anthropometry")
    kr_raw = L.read_recode(os.path.join(FIX, "XXKR7AFL.DTA"),
                           ["hw70", "hw71", "hw72", "hw73", "b5"], quiet=True)
    kr = L.clean_anthropometry(kr_raw, "KR", quiet=True)
    check("haz created", "haz" in kr.columns)
    check("flags at 9990 and above dropped", kr["haz"].max() < 6.001,
          f"max {kr['haz'].max()}")
    check("haz within WHO bounds",
          bool(((kr["haz"].dropna() >= -6) & (kr["haz"].dropna() <= 6)).all()))
    check("haz is a plausible z-score", -3 < kr["haz"].mean() < 0,
          f"mean {kr['haz'].mean():.3f}")
    check("some rows dropped as flagged", kr["haz"].isna().sum() > 0,
          f"{kr['haz'].isna().sum()} missing")
    # The PR prefix must not silently match the KR columns.
    pr_attempt = L.clean_anthropometry(kr_raw, "PR", quiet=True)
    check("PR prefix does not pick up hw70", "haz" not in pr_attempt.columns)

    print("century month codes")
    check("CMC 1441 is January 2020",
          tuple(int(x) for x in (lambda ym: (ym[0].iloc[0], ym[1].iloc[0]))(
              L.cmc_to_year_month(pd.Series([1441])))) == (2020, 1))
    check("CMC 1452 is December 2020",
          tuple(int(x) for x in (lambda ym: (ym[0].iloc[0], ym[1].iloc[0]))(
              L.cmc_to_year_month(pd.Series([1452])))) == (2020, 12))
    check("round trip", L.year_month_to_cmc(2020, 1) == 1441)

    print("missing variables are reported, not hidden")
    got = L.read_recode(os.path.join(FIX, "XXIR7AFL.DTA"),
                        ["v012", "sdist", "v456"], quiet=True)
    check("absent variables simply do not appear", "sdist" not in got.columns)
    check("present variables still load", "v012" in got.columns)

    print()
    if failures:
        print(f"FAIL: {len(failures)} check(s) failed: {', '.join(failures)}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
