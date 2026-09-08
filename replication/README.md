# replication

A replication package that can be verified, not just re-run.

```
python replication/run_all.py            # run from raw data, write output/, verify against the record
Rscript replication/run_regression.R     # the same model in R; run_all then checks the two agree
python replication/test_replication.py   # 4 tests, 12 checks
```

## What "verified" means here

`run_all.py` fits the model, writes every output, and compares the numbers a
reader would quote against `expected_results.json`. Any difference exits 1 and
names the result that moved. `--record` overwrites the record after a
deliberate change, and that change then shows in the diff of one small file.

`run_regression.R` fits the same model and writes the same key results, and
`verify.py` checks that Python and R agree on the point estimates, R-squared
and group means. They do, to six places. Standard errors are not compared,
because the Python uses HC1 and the R uses conventional errors; installing
`sandwich` was not worth it for a check on point estimates.

`test_replication.py` corrupts one outcome value in a copy and confirms the
verification fails. A verification step that cannot fail is not verifying
anything, and that test is the reason to trust the green run.

## Layout

| File | What it is |
|---|---|
| `data/simulated_study_data.csv` | 100 rows, synthetic. `id`, `treatment`, `age`, `income`, `outcome` |
| `analysis.py` | The model as functions: load, descriptives, fit, coefficient table, key results |
| `run_all.py` | Runs it end to end and verifies |
| `verify.py` | The comparison, and the Python-against-R check |
| `expected_results.json` | The record: eight numbers and the model spec |
| `run_regression.R` | The R cross-check |
| `output/` | Written on each run; not committed |

## Checklist for your own package

The structure is the point; the model is a placeholder. When you replace it:

1. **Data.** Raw data in `data/`, never edited by hand. If it cannot be
   shared, a `make_fixture.py` that builds a synthetic file with the same
   structure, as `data_starters/` does in this repository.
2. **One entry point.** A reader runs one command. Every intermediate file is
   produced by it, so nothing depends on a step that happened once on your
   laptop.
3. **Environment.** `output/environment.txt` records exact versions on every
   run. Pin them in a `requirements.txt` when you publish.
4. **The record.** Round the key results to what the data supports, store
   them, and compare exactly. A tolerance hides drift; rounding in one place
   does not.
5. **A second implementation** of the headline number, in another language or
   at least another library. Agreement between two independent routes is the
   cheapest strong evidence that neither is wrong.
6. **A test that the verification can fail.** Corrupt a value in a copy and
   confirm the run goes red.

## What this replaced

Two scripts, one Python and one R, each fitting the regression and writing a
text summary to a path that only resolved from inside `scripts/`. Nothing
compared them to each other or to anything, so a changed dataset produced a
different summary and no signal.
