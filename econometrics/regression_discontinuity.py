"""
Regression Discontinuity Design (RDD)
Exploits sharp cutoffs in eligibility to estimate causal effects.

Usage:
    python regression_discontinuity.py

Requires: pandas, numpy, statsmodels, matplotlib
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from pathlib import Path


def load_data(path=None):
    if path is None:
        path = Path(__file__).parent / "sample_program_data.csv"
    df = pd.read_csv(path)
    return df[df["post"] == 1].copy()  # Use post-treatment data


def sharp_rdd(df, outcome="outcome", running="running_var", cutoff=0.0):
    """
    Estimate sharp RDD effect using local linear regression.
    Treatment is assigned when running_var < cutoff.
    """
    df = df.copy()
    df["above"] = (df[running] >= cutoff).astype(int)
    df["centered"] = df[running] - cutoff

    # Local linear regression with different slopes on each side
    model = smf.ols(
        f"{outcome} ~ above + centered + above:centered", data=df
    ).fit()
    return model


def sharp_rdd_with_bandwidth(df, bandwidth=3.0, outcome="outcome", running="running_var", cutoff=0.0):
    """RDD restricted to observations within bandwidth of the cutoff."""
    df = df.copy()
    df = df[abs(df[running] - cutoff) <= bandwidth]
    if len(df) < 10:
        print(f"Warning: only {len(df)} observations within bandwidth {bandwidth}")
    return sharp_rdd(df, outcome, running, cutoff)


def mccrary_density_test(df, running="running_var", cutoff=0.0, bins=20):
    """
    Simple density test around the cutoff.
    If units can manipulate the running variable, we'd see a discontinuity in density.
    Returns bin counts below and above the cutoff.
    """
    below = df[df[running] < cutoff][running]
    above = df[df[running] >= cutoff][running]
    return {
        "n_below": len(below),
        "n_above": len(above),
        "ratio": round(len(below) / max(len(above), 1), 2),
        "concern": abs(len(below) - len(above)) / max(len(below) + len(above), 1) > 0.3,
    }


def plot_rdd(df, outcome="outcome", running="running_var", cutoff=0.0, output_path=None):
    """Scatter plot with fitted lines on each side of the cutoff."""
    fig, ax = plt.subplots(figsize=(8, 5))

    below = df[df[running] < cutoff]
    above = df[df[running] >= cutoff]

    ax.scatter(below[running], below[outcome], alpha=0.5, color="#1a56db", label="Below cutoff (treated)")
    ax.scatter(above[running], above[outcome], alpha=0.5, color="#9ca3af", label="Above cutoff (control)")

    # Fit lines
    for subset, color in [(below, "#1a56db"), (above, "#9ca3af")]:
        if len(subset) > 2:
            z = np.polyfit(subset[running], subset[outcome], 1)
            p = np.poly1d(z)
            x_line = np.linspace(subset[running].min(), subset[running].max(), 50)
            ax.plot(x_line, p(x_line), color=color, linewidth=2)

    ax.axvline(x=cutoff, color="red", linestyle="--", alpha=0.7, label="Cutoff")
    ax.set_xlabel("Running Variable")
    ax.set_ylabel(outcome.replace("_", " ").title())
    ax.set_title("Regression Discontinuity Design")
    ax.legend()
    plt.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=150)
    else:
        plt.show()
    plt.close()


if __name__ == "__main__":
    df = load_data()

    print("=== McCrary Density Test ===")
    density = mccrary_density_test(df)
    for k, v in density.items():
        print(f"  {k}: {v}")

    print("\n=== Sharp RDD Estimation ===")
    model = sharp_rdd(df)
    print(model.summary().tables[1])
    print(f"\n  RDD Effect (above coefficient): {model.params['above']:.2f}")
    print(f"  p-value: {model.pvalues['above']:.4f}")

    plot_rdd(df)
