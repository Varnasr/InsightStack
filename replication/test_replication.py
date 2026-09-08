"""Tests for the replication package. Run: python replication/test_replication.py

Checks that a clean run reproduces the record, and that a changed dataset is
caught. A verification step that cannot fail is not verifying anything.
"""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PASSED = 0


def check(cond, label):
    global PASSED
    if not cond:
        raise AssertionError(label)
    PASSED += 1


def run(cwd, *args):
    return subprocess.run([sys.executable, str(Path(cwd) / "run_all.py"), *args],
                          capture_output=True, text=True)


def test_clean_run_reproduces_the_record():
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copytree(HERE, Path(tmp) / "rep", ignore=shutil.ignore_patterns("output", "__pycache__"))
        r = run(Path(tmp) / "rep")
        check(r.returncode == 0, f"clean run verifies: {r.stdout}{r.stderr}")
        check("REPLICATION OK" in r.stdout, "says so")
        out = Path(tmp) / "rep" / "output"
        for f in ("descriptives.csv", "coefficients.csv", "model_summary.txt",
                  "key_results.json", "environment.txt"):
            check((out / f).exists(), f"writes {f}")


def test_a_changed_dataset_fails_verification():
    with tempfile.TemporaryDirectory() as tmp:
        dst = Path(tmp) / "rep"
        shutil.copytree(HERE, dst, ignore=shutil.ignore_patterns("output", "__pycache__"))
        data = dst / "data" / "simulated_study_data.csv"
        lines = data.read_text().splitlines()
        parts = lines[1].split(","); parts[-1] = str(float(parts[-1]) + 50); lines[1] = ",".join(parts)
        data.write_text("\n".join(lines) + "\n")
        r = run(dst)
        check(r.returncode == 1, "a changed outcome value fails verification")
        check("REPLICATION FAILED" in r.stdout and "treatment_estimate" in r.stdout,
              "and names the result that moved")


def test_record_mode_rewrites_the_expected_file():
    with tempfile.TemporaryDirectory() as tmp:
        dst = Path(tmp) / "rep"
        shutil.copytree(HERE, dst, ignore=shutil.ignore_patterns("output", "__pycache__"))
        (dst / "expected_results.json").write_text("{}")
        check(run(dst).returncode == 1, "an empty record fails")
        check(run(dst, "--record").returncode == 0, "--record rewrites it")
        check(run(dst).returncode == 0, "and the next run passes")
        rec = json.loads((dst / "expected_results.json").read_text())
        check(rec["n"] == 100, "with the real results")


def test_duplicate_ids_are_refused():
    with tempfile.TemporaryDirectory() as tmp:
        dst = Path(tmp) / "rep"
        shutil.copytree(HERE, dst, ignore=shutil.ignore_patterns("output", "__pycache__"))
        data = dst / "data" / "simulated_study_data.csv"
        lines = data.read_text().splitlines(); lines.append(lines[1])
        data.write_text("\n".join(lines) + "\n")
        r = run(dst)
        check(r.returncode != 0 and "duplicate ids" in r.stderr, "duplicate id refused")


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in tests:
        fn(); print(f"  ok  {fn.__name__}")
    print(f"\n{len(tests)} tests, {PASSED} checks, all passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
