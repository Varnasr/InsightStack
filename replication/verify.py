"""Compare a run's key results with the recorded ones. Exit 1 on any difference.

    python replication/verify.py       # compares output/key_results.json to expected_results.json

Exact comparison on integers and the model spec, and on the rounded floats,
because both sides were rounded to six places by `analysis.key_results` before
being written. If a platform difference ever shows up in the sixth decimal,
loosen the rounding there, in one place, rather than adding a tolerance here.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def compare(got: dict, expected: dict) -> int:
    problems = []
    for k, v in expected.items():
        if k not in got:
            problems.append(f"{k}: missing from this run")
        elif got[k] != v:
            problems.append(f"{k}: expected {v!r}, got {got[k]!r}")
    for k in got:
        if k not in expected:
            problems.append(f"{k}: produced by this run but not in the record")
    if problems:
        print("REPLICATION FAILED")
        for p in problems:
            print("  " + p)
        return 1
    print(f"REPLICATION OK: {len(expected)} recorded results reproduced")
    return 0


def compare_with_r(got: dict) -> int:
    """If run_regression.R has written its results, check the two agree.

    Only the fields both produce: n, r_squared, the treatment estimate, and the
    two group means. Standard errors differ by design (HC1 against
    conventional) and are not compared.
    """
    path = HERE / "output" / "key_results_r.json"
    if not path.exists():
        print("R results not present; skipped (run Rscript replication/run_regression.R)")
        return 0
    r = json.loads(path.read_text())
    problems = [f"{k}: python {got[k]!r}, R {r[k]!r}" for k in r if k in got and got[k] != r[k]]
    if problems:
        print("PYTHON AND R DISAGREE")
        for p in problems:
            print("  " + p)
        return 1
    print(f"Python and R agree on {len(r)} results")
    return 0


def main() -> int:
    got = json.loads((HERE / "output" / "key_results.json").read_text())
    expected = json.loads((HERE / "expected_results.json").read_text())
    return compare(got, expected) or compare_with_r(got)


if __name__ == "__main__":
    sys.exit(main())
