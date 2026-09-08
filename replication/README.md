# replication

A replication package with one entry point, a recorded result and a check
that the run still matches it.

```
python replication/run_all.py            # run from raw data, write output/, verify against the record
Rscript replication/run_regression.R     # the same model in R
python replication/test_replication.py   # 4 tests, 12 checks
```

`run_all.py` fits the model, writes every output, and compares the key
results with `expected_results.json`. Any difference exits 1 and names the
result that moved. `--record` overwrites the record after a deliberate
change.

`run_regression.R` fits the same model in R. `verify.py` checks that Python
and R agree on point estimates, R-squared and group means, to six places.
Standard errors are not compared: the Python uses HC1, the R uses
conventional errors.

`test_replication.py` corrupts one value in a copy and confirms the
verification fails.

## Files

| File | What it is |
| --- | --- |
| `data/simulated_study_data.csv` | 100 synthetic rows: `id`, `treatment`, `age`, `income`, `outcome` |
| `analysis.py` | The model as functions: load, descriptives, fit, coefficient table, key results |
| `run_all.py` | Runs it end to end and verifies |
| `verify.py` | The comparison, and the Python-against-R check |
| `expected_results.json` | Eight numbers and the model spec |
| `run_regression.R` | The R cross-check |
| `output/` | Written on each run; not committed |

## Using the structure for your own package

1. Raw data in `data/`, never edited by hand. If it cannot be shared, a
   `make_fixture.py` that builds a synthetic file with the same structure.
2. One entry point that produces every intermediate file.
3. `output/environment.txt` records versions on every run; pin them in a
   `requirements.txt` when you publish.
4. Round the key results to what the data supports, store them, and compare
   exactly.
5. A second implementation of the headline number, in another language or
   another library.
6. A test that the verification can fail.
