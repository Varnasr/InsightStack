"""
Sensitivity Analysis for Causal Claims
Rosenbaum bounds and placebo tests to assess robustness.

Usage:
    python sensitivity_analysis.py

Requires: pandas, numpy, scipy
"""

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path


def load_data(path=None):
    if path is None:
        path = Path(__file__).parent / "sample_program_data.csv"
    return pd.read_csv(path)


def rosenbaum_bounds(treated_outcomes, control_outcomes, gamma_range=None):
    """
    Rosenbaum bounds test for sensitivity to hidden bias.

    Gamma (G) represents how much an unobserved confounder could change
    the odds of treatment assignment. G=1 means no hidden bias.
    Higher G values test robustness to stronger confounders.
    """
    if gamma_range is None:
        gamma_range = [1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0]

    # Observed test statistic (simple t-test)
    t_stat, p_value = stats.ttest_ind(treated_outcomes, control_outcomes)
    n_t = len(treated_outcomes)
    n_c = len(control_outcomes)
    diff = treated_outcomes.mean() - control_outcomes.mean()

    results = []
    for gamma in gamma_range:
        # Under hidden bias of magnitude gamma, the p-value bounds shift
        # Simplified approximation using the odds ratio adjustment
        adjusted_p_upper = min(p_value * gamma, 1.0)
        adjusted_p_lower = max(p_value / gamma, 0.0)

        results.append({
            "gamma": gamma,
            "p_lower": round(adjusted_p_lower, 4),
            "p_upper": round(adjusted_p_upper, 4),
            "significant_at_05": adjusted_p_upper < 0.05,
        })

    return {
        "observed_diff": round(diff, 3),
        "observed_t": round(t_stat, 3),
        "observed_p": round(p_value, 4),
        "bounds": pd.DataFrame(results),
    }


def placebo_test(df, outcome="outcome", treatment="treatment",
                 placebo_var="education_years"):
    """
    Placebo test: Check if treatment predicts a variable it shouldn't.
    If treatment is randomly assigned, it should not predict pre-treatment covariates.
    """
    treated = df[df[treatment] == 1][placebo_var]
    control = df[df[treatment] == 0][placebo_var]

    t_stat, p_value = stats.ttest_ind(treated, control)
    return {
        "placebo_variable": placebo_var,
        "treated_mean": round(treated.mean(), 3),
        "control_mean": round(control.mean(), 3),
        "t_statistic": round(t_stat, 3),
        "p_value": round(p_value, 4),
        "passes": p_value > 0.05,  # No significant difference is good
    }


def permutation_test(treated_outcomes, control_outcomes, n_permutations=1000):
    """
    Permutation test for the treatment effect.
    Randomly reassigns treatment labels and computes the test statistic
    to build a null distribution.
    """
    observed_diff = treated_outcomes.mean() - control_outcomes.mean()
    combined = np.concatenate([treated_outcomes, control_outcomes])
    n_t = len(treated_outcomes)

    np.random.seed(42)
    null_diffs = []
    for _ in range(n_permutations):
        perm = np.random.permutation(combined)
        null_diffs.append(perm[:n_t].mean() - perm[n_t:].mean())

    null_diffs = np.array(null_diffs)
    p_value = (np.abs(null_diffs) >= np.abs(observed_diff)).mean()

    return {
        "observed_diff": round(observed_diff, 3),
        "permutation_p_value": round(p_value, 4),
        "n_permutations": n_permutations,
    }


if __name__ == "__main__":
    df = load_data()
    post = df[df["post"] == 1]
    treated = post[post["treatment"] == 1]["outcome"].values
    control = post[post["treatment"] == 0]["outcome"].values

    print("=== Rosenbaum Bounds ===")
    bounds = rosenbaum_bounds(treated, control)
    print(f"  Observed difference: {bounds['observed_diff']}")
    print(f"  Observed p-value: {bounds['observed_p']}")
    print(bounds["bounds"].to_string(index=False))

    print("\n=== Placebo Tests ===")
    pre = df[df["post"] == 0]
    for var in ["age", "female", "education_years", "income_baseline"]:
        result = placebo_test(pre, placebo_var=var)
        status = "PASS" if result["passes"] else "FAIL"
        print(f"  {var}: p={result['p_value']} [{status}]")

    print("\n=== Permutation Test ===")
    perm = permutation_test(treated, control)
    print(f"  Observed diff: {perm['observed_diff']}")
    print(f"  Permutation p-value: {perm['permutation_p_value']}")
