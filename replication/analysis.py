"""The analysis, as functions, so `run_all.py` can run it and `verify.py` can check it.

One model: outcome on treatment, age and income, OLS with heteroskedasticity-
robust (HC1) standard errors. The point of this folder is not the model, which
is deliberately plain; it is that the model, its data, its environment and its
expected output sit together and a stranger can confirm they still agree.

Nothing here prints. Functions return frames and dicts; the runner writes them.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE / "data" / "simulated_study_data.csv"

MODEL = {"outcome": "outcome", "predictors": ["treatment", "age", "income"], "cov": "HC1"}


def load_data(path=DATA) -> pd.DataFrame:
    df = pd.read_csv(path)
    needed = [MODEL["outcome"], *MODEL["predictors"], "id"]
    missing = [c for c in needed if c not in df.columns]
    if missing:
        raise ValueError(f"{path}: missing column(s) {missing}")
    if df["id"].duplicated().any():
        raise ValueError(f"{path}: duplicate ids; the analysis assumes one row per unit")
    return df


def descriptives(df: pd.DataFrame) -> pd.DataFrame:
    cols = [MODEL["outcome"], *MODEL["predictors"]]
    out = df[cols].agg(["count", "mean", "std", "min", "max"]).T
    out.index.name = "variable"
    return out.reset_index()


def fit(df: pd.DataFrame):
    import statsmodels.api as sm

    X = sm.add_constant(df[MODEL["predictors"]].astype(float))
    y = df[MODEL["outcome"]].astype(float)
    return sm.OLS(y, X).fit(cov_type=MODEL["cov"])


def coefficient_table(result) -> pd.DataFrame:
    ci = result.conf_int()
    return pd.DataFrame({
        "term": result.params.index,
        "estimate": result.params.values,
        "std_error": result.bse.values,
        "t": result.tvalues.values,
        "p_value": result.pvalues.values,
        "ci_low": ci[0].values,
        "ci_high": ci[1].values,
    })


def key_results(result, df: pd.DataFrame) -> dict:
    """The numbers a reader would quote, rounded to what the data can support.

    These are what `expected_results.json` stores and `verify.py` compares. Six
    decimal places, which is far inside floating-point agreement across
    platforms and far outside anything a substantive change would leave alone.
    """
    return {
        "n": int(result.nobs),
        "r_squared": round(float(result.rsquared), 6),
        "treatment_estimate": round(float(result.params["treatment"]), 6),
        "treatment_std_error": round(float(result.bse["treatment"]), 6),
        "treatment_p_value": round(float(result.pvalues["treatment"]), 6),
        "outcome_mean_control": round(float(df.loc[df.treatment == 0, "outcome"].mean()), 6),
        "outcome_mean_treated": round(float(df.loc[df.treatment == 1, "outcome"].mean()), 6),
        "model": MODEL,
    }
