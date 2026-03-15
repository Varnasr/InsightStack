"""
Difference-in-Differences (DiD) Estimation
Compares changes over time between treatment and control groups.

Usage:
    python difference_in_differences.py

Requires: pandas, statsmodels, matplotlib
"""

import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from pathlib import Path


def load_data(path=None):
    if path is None:
        path = Path(__file__).parent / "sample_program_data.csv"
    return pd.read_csv(path)


def estimate_did(df, outcome="outcome", treatment="treatment", post="post"):
    """
    Estimate DiD using OLS regression:
    outcome = b0 + b1*treatment + b2*post + b3*(treatment*post) + e

    b3 is the DiD estimator (average treatment effect on the treated).
    """
    df = df.copy()
    df["treat_post"] = df[treatment] * df[post]

    model = smf.ols(f"{outcome} ~ {treatment} + {post} + treat_post", data=df).fit()
    return model


def estimate_did_with_covariates(df, covariates=None):
    """DiD with control variables for improved precision."""
    if covariates is None:
        covariates = ["age", "female", "education_years"]

    df = df.copy()
    df["treat_post"] = df["treatment"] * df["post"]
    covar_str = " + ".join(covariates)
    formula = f"outcome ~ treatment + post + treat_post + {covar_str}"

    model = smf.ols(formula, data=df).fit()
    return model


def parallel_trends_test(df):
    """
    Test parallel trends assumption using pre-treatment data only.
    If treatment and control groups have similar pre-trends, DiD is valid.
    """
    pre = df[df["post"] == 0]
    treat_mean = pre[pre["treatment"] == 1]["outcome"].mean()
    control_mean = pre[pre["treatment"] == 0]["outcome"].mean()
    return {
        "treatment_pre_mean": round(treat_mean, 2),
        "control_pre_mean": round(control_mean, 2),
        "pre_treatment_gap": round(treat_mean - control_mean, 2),
    }


def plot_did(df, output_path=None):
    """Visualise the DiD estimate with group means over time."""
    means = df.groupby(["treatment", "post"])["outcome"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(7, 4))
    for treat, label, color in [(1, "Treatment", "#1a56db"), (0, "Control", "#9ca3af")]:
        group = means[means["treatment"] == treat]
        ax.plot(group["post"], group["outcome"], "o-", label=label, color=color, linewidth=2)

    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Pre", "Post"])
    ax.set_ylabel("Outcome")
    ax.set_title("Difference-in-Differences")
    ax.legend()
    plt.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=150)
    else:
        plt.show()
    plt.close()


if __name__ == "__main__":
    df = load_data()

    print("=== Parallel Trends Test ===")
    trends = parallel_trends_test(df)
    for k, v in trends.items():
        print(f"  {k}: {v}")

    print("\n=== DiD Estimation (Basic) ===")
    model = estimate_did(df)
    print(model.summary().tables[1])
    print(f"\n  ATT (treat_post coefficient): {model.params['treat_post']:.2f}")
    print(f"  p-value: {model.pvalues['treat_post']:.4f}")

    print("\n=== DiD with Covariates ===")
    model_cov = estimate_did_with_covariates(df)
    print(model_cov.summary().tables[1])
    print(f"\n  ATT: {model_cov.params['treat_post']:.2f}")

    plot_did(df)
