"""Peer effects, and why the obvious regression does not measure them.

The question is whether a woman saves more because the other members of her
self-help group save more. The obvious regression is her savings on the group's
average savings, and it is the textbook example of a specification that cannot
answer the question it is written for.

Manski (1993) calls it the reflection problem, and it has three parts that a
positive coefficient cannot distinguish between:

  ENDOGENOUS effects   her behaviour responds to her peers' behaviour.
                       This is the thing you want to measure.
  EXOGENOUS effects    her behaviour responds to her peers' characteristics:
                       older group members, more educated ones.
  CORRELATED effects   she and her peers behave alike because they face the
                       same village, the same bank, the same rainfall, or
                       because they chose each other in the first place.

With groups this shape, the three are not separately identified. That is a
property of the design, not a defect in the estimator, and no amount of
controls fixes it: the leave-one-out mean removes the mechanical simultaneity
and leaves the identification problem exactly where it was.

So this module estimates the association and labels it an association. It does
two things a naive version does not:

1. Leave-one-out peer means, computed in closed form rather than row by row.
   Including a member's own value in the mean she is regressed on guarantees a
   positive coefficient from arithmetic alone.
2. Group-size and village controls, and an optional village fixed effect, which
   absorbs the correlated effects that operate at village level. It does not
   touch the ones operating at group level, which for a self-selected group is
   most of them.

What would identify it: exogenous variation in group composition. Randomised
assignment to groups; or, in an observed network, the intransitive structure
Bramoullé, Djebbari and Fortin (2009) exploit, where a friend's friend who is
not your friend supplies the excluded instrument. Fully connected groups like
these have no such structure, which is why the answer here stops at
"associated" and says so in the printed output.

References: Manski, "Identification of endogenous social effects: the reflection
problem", *Review of Economic Studies* 60(3), 1993, 531-542. Bramoullé,
Djebbari and Fortin, "Identification of peer effects through social networks",
*Journal of Econometrics* 150(1), 2009, 41-55.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .network import attach_centrality

__all__ = ["leave_one_out_mean", "peer_association"]

DATA = Path(__file__).resolve().parent / "data"


def leave_one_out_mean(df: pd.DataFrame, value: str, group: str) -> pd.Series:
    """Mean of ``value`` over a member's group, excluding the member.

    Closed form: ``(group_sum - own) / (group_n - 1)``. The row-by-row filter
    this replaces was O(n²) and, more importantly, the version that includes the
    member's own value guarantees a positive coefficient from arithmetic alone,
    because the regressor contains the dependent variable.

    A member who is alone in their group has no peers, so the result is NaN
    rather than their own value. Substituting their own value there is the same
    error in miniature, and on a survey with many singleton groups it is enough
    to produce the finding on its own.
    """
    for col in (value, group):
        if col not in df.columns:
            raise KeyError(f"leave_one_out_mean: no column {col!r} in the frame")

    grouped = df.groupby(group)[value]
    total = grouped.transform("sum")
    count = grouped.transform("count")
    own = df[value]
    with np.errstate(invalid="ignore", divide="ignore"):
        out = (total - own) / (count - 1)
    return out.where(count > 1)


def peer_association(df: pd.DataFrame, *, outcome: str = "monthly_savings",
                     group: str = "peer_group_id", village: str | None = "village",
                     controls: tuple[str, ...] = ("age", "education_years"),
                     village_fixed_effects: bool = True) -> dict:
    """Association between a member's outcome and her peers' mean outcome.

    Deliberately not called `estimate_peer_effect`. The returned dict carries an
    ``interpretation`` string that says what the coefficient is and is not, and
    `print_result` prints it, because a number this easy to mislabel should not
    travel without its caveat.

    Members alone in their group are dropped, and the count is reported.
    """
    import statsmodels.api as sm

    needed = [outcome, group, *controls] + ([village] if village else [])
    missing = [c for c in needed if c not in df.columns]
    if missing:
        raise KeyError(f"peer_association: no column(s) {missing} in the frame")

    work = df.copy()
    work["peer_mean"] = leave_one_out_mean(work, outcome, group)
    work["group_size"] = work.groupby(group)[outcome].transform("count")

    n_before = len(work)
    work = work.dropna(subset=["peer_mean", outcome, *controls])
    dropped = n_before - len(work)
    if len(work) <= len(controls) + 3:
        raise ValueError(
            f"peer_association: {len(work)} usable rows for {len(controls) + 3} "
            "parameters. Most members are alone in their group.")

    X = work[["peer_mean", "group_size", *controls]].astype(float)
    note_fe = "none"
    if village_fixed_effects and village:
        dummies = pd.get_dummies(work[village], prefix="village", drop_first=True,
                                 dtype=float)
        if dummies.shape[1] == 0:
            note_fe = f"requested, but {village!r} takes one value"
        else:
            X = pd.concat([X, dummies], axis=1)
            note_fe = f"{village} ({dummies.shape[1] + 1} levels)"
    X = sm.add_constant(X)

    # Clustered at the group, because members of a group share whatever the
    # group does. Conventional standard errors here are far too small.
    fit = sm.OLS(work[outcome].astype(float), X).fit(
        cov_type="cluster", cov_kwds={"groups": work[group]})

    coef = float(fit.params["peer_mean"])
    se = float(fit.bse["peer_mean"])
    lo, hi = fit.conf_int().loc["peer_mean"].tolist()

    return {
        "coefficient": coef, "std_error": se,
        "conf_int": (float(lo), float(hi)),
        "p_value": float(fit.pvalues["peer_mean"]),
        "n": int(fit.nobs), "n_groups": int(work[group].nunique()),
        "dropped_singletons": int(dropped),
        "fixed_effects": note_fe,
        "std_errors": f"clustered on {group}",
        "interpretation": (
            "This is an association, not a peer effect. A member whose group "
            "saves 100 rupees more per month is associated with saving "
            f"{coef:.1f} rupees more herself. Endogenous influence, response to "
            "peers' characteristics, and shared circumstances or self-selection "
            "into groups are not separately identified in fully connected "
            "groups (Manski 1993). Identifying the first needs exogenous "
            "variation in who is grouped with whom."),
        "model": fit,
    }


def print_result(result: dict) -> None:
    """Print the estimate with its caveat attached, in that order."""
    print(f"Peer mean coefficient: {result['coefficient']:.4f} "
          f"(se {result['std_error']:.4f}, {result['std_errors']})")
    print(f"95% CI: [{result['conf_int'][0]:.4f}, {result['conf_int'][1]:.4f}]  "
          f"p = {result['p_value']:.4f}")
    print(f"n = {result['n']} across {result['n_groups']} groups; "
          f"{result['dropped_singletons']} singleton(s) dropped; "
          f"fixed effects: {result['fixed_effects']}")
    print()
    print(result["interpretation"])
