"""
Propensity Score Matching (PSM)
Matches treatment and control units based on observable characteristics.

Usage:
    python propensity_score_matching.py

Requires: pandas, numpy, statsmodels, scipy
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy.spatial.distance import cdist
from pathlib import Path


def load_data(path=None):
    if path is None:
        path = Path(__file__).parent / "sample_program_data.csv"
    df = pd.read_csv(path)
    return df[df["post"] == 0].copy()  # Use baseline data only


def estimate_propensity_scores(df, covariates=None):
    """Estimate propensity scores using logistic regression."""
    if covariates is None:
        covariates = ["age", "female", "education_years", "income_baseline"]

    X = sm.add_constant(df[covariates])
    y = df["treatment"]
    model = sm.Logit(y, X).fit(disp=0)
    df = df.copy()
    df["pscore"] = model.predict(X)
    return df, model


def nearest_neighbor_match(df, caliper=0.1):
    """
    Match each treated unit to nearest control unit by propensity score.
    Caliper restricts matches to those within a maximum distance.
    """
    treated = df[df["treatment"] == 1].copy()
    control = df[df["treatment"] == 0].copy()

    matches = []
    used_controls = set()

    for _, t_row in treated.iterrows():
        distances = abs(control["pscore"] - t_row["pscore"])
        # Exclude already-used controls (without replacement)
        distances[control.index.isin(used_controls)] = np.inf

        if distances.min() <= caliper:
            match_idx = distances.idxmin()
            used_controls.add(match_idx)
            matches.append({
                "treated_id": t_row["id"],
                "control_id": control.loc[match_idx, "id"],
                "treated_pscore": t_row["pscore"],
                "control_pscore": control.loc[match_idx, "pscore"],
                "distance": distances.min(),
            })

    return pd.DataFrame(matches)


def assess_balance(df, matches_df, covariates=None):
    """Check covariate balance between matched treatment and control groups."""
    if covariates is None:
        covariates = ["age", "female", "education_years", "income_baseline"]

    treated_ids = matches_df["treated_id"].values
    control_ids = matches_df["control_id"].values

    treated = df[df["id"].isin(treated_ids)]
    control = df[df["id"].isin(control_ids)]

    balance = []
    for var in covariates:
        t_mean = treated[var].mean()
        c_mean = control[var].mean()
        pooled_sd = np.sqrt((treated[var].var() + control[var].var()) / 2)
        std_diff = (t_mean - c_mean) / pooled_sd if pooled_sd > 0 else 0

        balance.append({
            "variable": var,
            "treated_mean": round(t_mean, 2),
            "control_mean": round(c_mean, 2),
            "std_diff": round(std_diff, 3),
            "balanced": abs(std_diff) < 0.1,
        })

    return pd.DataFrame(balance)


def estimate_att(df, matches_df, outcome="baseline_outcome"):
    """Estimate Average Treatment Effect on the Treated (ATT)."""
    treated = df[df["id"].isin(matches_df["treated_id"])]
    control = df[df["id"].isin(matches_df["control_id"])]

    att = treated[outcome].mean() - control[outcome].mean()
    se = np.sqrt(treated[outcome].var() / len(treated) + control[outcome].var() / len(control))
    return {"att": round(att, 3), "se": round(se, 3), "n_matched": len(matches_df)}


if __name__ == "__main__":
    df = load_data()

    print("=== Propensity Score Estimation ===")
    df, model = estimate_propensity_scores(df)
    print(f"  Treatment group mean pscore: {df[df['treatment']==1]['pscore'].mean():.3f}")
    print(f"  Control group mean pscore: {df[df['treatment']==0]['pscore'].mean():.3f}")

    print("\n=== Nearest Neighbor Matching ===")
    matches = nearest_neighbor_match(df, caliper=0.2)
    print(f"  Matched pairs: {len(matches)}")
    print(f"  Mean distance: {matches['distance'].mean():.4f}")

    print("\n=== Covariate Balance ===")
    balance = assess_balance(df, matches)
    print(balance.to_string(index=False))

    print("\n=== ATT Estimate ===")
    att = estimate_att(df, matches)
    print(f"  ATT: {att['att']}")
    print(f"  SE: {att['se']}")
    print(f"  Matched pairs: {att['n_matched']}")
