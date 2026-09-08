"""
Build small synthetic files shaped like DHS recodes, so the loaders can be tested
without the real microdata.

The DHS data licence does not let anyone redistribute the recode files, and the
files are large besides. These fixtures carry the structure that matters (raw
weights near a million, hw70-hw73 stored times 100 with flags at 9990 and above,
century month codes, the mv- prefix in the men's recode) and nothing else. They
are not data about anybody. Every value is drawn from a seeded generator.

    python make_fixture.py --outdir fixtures
"""

from __future__ import annotations

import argparse
import os

import numpy as np
import pandas as pd
import pyreadstat

SEED = 20260908


def _women(n: int, rng: np.random.Generator) -> pd.DataFrame:
    cluster = rng.integers(1, 41, n)
    return pd.DataFrame({
        "v001": cluster,
        "v002": rng.integers(1, 30, n),
        "v003": rng.integers(1, 9, n),
        # Raw DHS weights average about a million because they are stored with
        # six implied decimals.
        "v005": rng.normal(1_000_000, 180_000, n).clip(50_000).round(),
        "v008": rng.integers(1430, 1456, n),          # interview date, CMC
        "v012": rng.integers(15, 50, n),
        "v021": cluster,
        "v022": (cluster % 8) + 1,
        "v024": rng.integers(1, 6, n),
        "v025": rng.integers(1, 3, n),
        "v106": rng.integers(0, 4, n),
        "v133": rng.integers(0, 17, n),
        "v190": rng.integers(1, 6, n),
        "v191": rng.normal(0, 100_000, n).round(),     # score, times 100,000
        "v201": rng.poisson(2.1, n),
        "v437": rng.normal(510, 90, n).clip(250).round(),   # kg times 10
        "v438": rng.normal(1520, 65, n).round(),            # cm times 10
    })


def _children(n: int, rng: np.random.Generator) -> pd.DataFrame:
    df = _women(n, rng)
    df["b3"] = rng.integers(1380, 1450, n)
    df["b4"] = rng.integers(1, 3, n)
    df["b5"] = (rng.random(n) > 0.04).astype(int)
    for col, mean in (("hw70", -140), ("hw71", -110), ("hw72", -60), ("hw73", -55)):
        z = rng.normal(mean, 130, n).round()
        # About one in twelve children carries a flag or a missing value.
        flagged = rng.random(n) < 0.08
        z[flagged] = rng.choice([9996, 9997, 9998, 9999], flagged.sum())
        df[col] = z
    return df


def _men(n: int, rng: np.random.Generator) -> pd.DataFrame:
    w = _women(n, rng)
    men = w.rename(columns={c: "m" + c for c in w.columns if c.startswith("v")})
    men["mv012"] = rng.integers(15, 55, n)
    return men.drop(columns=[c for c in ("mv201", "mv437", "mv438") if c in men.columns])


def _household(n: int, rng: np.random.Generator) -> pd.DataFrame:
    cluster = rng.integers(1, 41, n)
    return pd.DataFrame({
        "hv001": cluster,
        "hv002": rng.integers(1, 30, n),
        "hv005": rng.normal(1_000_000, 200_000, n).clip(50_000).round(),
        "hv008": rng.integers(1430, 1456, n),
        "hv021": cluster,
        "hv022": (cluster % 8) + 1,
        "hv024": rng.integers(1, 6, n),
        "hv025": rng.integers(1, 3, n),
        "hv270": rng.integers(1, 6, n),
        "hv271": rng.normal(0, 100_000, n).round(),
    })


BUILDERS = {
    "XXIR7AFL.DTA": ("IR", _women, 900),
    "XXKR7AFL.DTA": ("KR", _children, 700),
    "XXMR7AFL.DTA": ("MR", _men, 400),
    "XXHR7AFL.DTA": ("HR", _household, 500),
}


def build(outdir: str) -> list[str]:
    os.makedirs(outdir, exist_ok=True)
    written = []
    for name, (_recode, builder, n) in BUILDERS.items():
        rng = np.random.default_rng(SEED + len(name))
        df = builder(n, rng).astype("float64")
        path = os.path.join(outdir, name)
        pyreadstat.write_dta(df, path)
        written.append(path)
    return written


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--outdir", default="fixtures")
    args = p.parse_args()
    for path in build(args.outdir):
        print(f"wrote {path}")
