"""Run the whole analysis from raw data to outputs, then verify against the record.

    python replication/run_all.py            # run, write output/, verify
    python replication/run_all.py --record   # run, and overwrite expected_results.json

Writes to `output/`: descriptives.csv, coefficients.csv, model_summary.txt,
key_results.json, and environment.txt (the exact package versions that
produced them). Then compares key_results.json with expected_results.json and
exits 1 on any difference, so a replication that has drifted fails loudly.
"""

from __future__ import annotations

import argparse
import json
import platform
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analysis  # noqa: E402
import verify  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
EXPECTED = HERE / "expected_results.json"


def environment() -> str:
    import numpy, pandas, statsmodels, scipy
    return "\n".join([
        f"python {platform.python_version()} ({platform.system()} {platform.machine()})",
        f"numpy {numpy.__version__}", f"pandas {pandas.__version__}",
        f"scipy {scipy.__version__}", f"statsmodels {statsmodels.__version__}",
    ]) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--record", action="store_true",
                    help="overwrite expected_results.json with this run's results")
    args = ap.parse_args(argv)

    OUT.mkdir(exist_ok=True)
    df = analysis.load_data()
    result = analysis.fit(df)

    analysis.descriptives(df).to_csv(OUT / "descriptives.csv", index=False)
    analysis.coefficient_table(result).to_csv(OUT / "coefficients.csv", index=False)
    (OUT / "model_summary.txt").write_text(result.summary().as_text() + "\n")
    key = analysis.key_results(result, df)
    (OUT / "key_results.json").write_text(json.dumps(key, indent=2) + "\n")
    (OUT / "environment.txt").write_text(environment())
    print(f"ran on {len(df)} rows; outputs in {OUT.relative_to(HERE.parent)}/")

    if args.record:
        EXPECTED.write_text(json.dumps(key, indent=2) + "\n")
        print(f"recorded {EXPECTED.name}")
        return 0
    return verify.compare(key, json.loads(EXPECTED.read_text())) or verify.compare_with_r(key)


if __name__ == "__main__":
    sys.exit(main())
