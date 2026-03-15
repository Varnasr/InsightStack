"""
Instrumental Variables (2SLS) Estimation
Uses an external instrument to address endogeneity.

Usage:
    python instrumental_variables.py

Requires: pandas, numpy, statsmodels
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from pathlib import Path


def load_data(path=None):
    """Load data and create a simulated instrument (distance to program office)."""
    if path is None:
        path = Path(__file__).parent / "sample_program_data.csv"
    df = pd.read_csv(path)
    df = df[df["post"] == 1].copy()

    # Simulate instrument: distance to program office (correlated with treatment, not outcome)
    np.random.seed(42)
    df["distance_km"] = np.where(
        df["treatment"] == 1,
        np.random.uniform(1, 15, len(df)),
        np.random.uniform(10, 30, len(df)),
    )
    return df


def two_stage_least_squares(df, outcome="outcome", endogenous="treatment",
                             instrument="distance_km", covariates=None):
    """
    Manual 2SLS estimation:
    Stage 1: Regress endogenous variable on instrument + covariates
    Stage 2: Regress outcome on predicted endogenous + covariates
    """
    if covariates is None:
        covariates = ["age", "female", "education_years"]

    exog_vars = [instrument] + covariates
    X_first = sm.add_constant(df[exog_vars])
    y_first = df[endogenous]

    # First stage
    first_stage = sm.OLS(y_first, X_first).fit()
    df = df.copy()
    df["treatment_hat"] = first_stage.predict(X_first)

    # Second stage
    X_second = sm.add_constant(df[["treatment_hat"] + covariates])
    y_second = df[outcome]
    second_stage = sm.OLS(y_second, X_second).fit()

    return first_stage, second_stage


def first_stage_ftest(first_stage_model, instrument="distance_km"):
    """
    Check instrument strength via first-stage F-statistic.
    Rule of thumb: F > 10 indicates a strong instrument.
    """
    f_stat = first_stage_model.fvalue
    return {
        "f_statistic": round(f_stat, 2),
        "strong_instrument": f_stat > 10,
        "instrument_coef": round(first_stage_model.params.get(instrument, 0), 4),
        "instrument_pvalue": round(first_stage_model.pvalues.get(instrument, 1), 4),
    }


if __name__ == "__main__":
    df = load_data()

    print("=== 2SLS Estimation ===")
    first, second = two_stage_least_squares(df)

    print("\nFirst Stage (Treatment ~ Distance + Covariates):")
    print(first.summary().tables[1])

    print("\nFirst Stage Diagnostics:")
    diag = first_stage_ftest(first)
    for k, v in diag.items():
        print(f"  {k}: {v}")

    print("\nSecond Stage (Outcome ~ Treatment_hat + Covariates):")
    print(second.summary().tables[1])
    print(f"\n  IV Estimate (treatment_hat): {second.params['treatment_hat']:.2f}")
