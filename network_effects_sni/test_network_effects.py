"""Tests for network_effects_sni.

Run: python -m network_effects_sni.test_network_effects

Plain asserts and a main(), matching the data_starters suites in this
repository, so the whole thing runs under CI without a test runner.

The checks that matter are the two that catch the errors the previous version
of this folder made: a peer mean that includes the member's own value, and a
diffusion simulation whose answer changes between runs.
"""

import sys
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd

from .diffusion import compare_strategies, seed_strategies, simulate_diffusion
from .network import attach_centrality, build_group_graph, centrality_table
from .peer_effects import leave_one_out_mean, peer_association

DATA = Path(__file__).resolve().parent / "data"
PASSED = 0


def check(condition, label):
    global PASSED
    if not condition:
        raise AssertionError(label)
    PASSED += 1


def sample():
    return pd.read_csv(DATA / "shg_peer_influence.csv")


# ---------------------------------------------------------------- network ---

def test_graph_is_one_clique_per_group():
    df = pd.DataFrame({"id": [1, 2, 3, 4, 5], "peer_group_id": [1, 1, 1, 2, 2]})
    g = build_group_graph(df)
    check(g.number_of_nodes() == 5, "every member is a node")
    check(g.number_of_edges() == 3 + 1, "3 edges in a triangle, 1 in a pair")
    check(nx.number_connected_components(g) == 2, "groups are disconnected")


def test_a_member_alone_in_a_group_is_a_node_with_no_edges():
    df = pd.DataFrame({"id": [1, 2, 3], "peer_group_id": [1, 1, 9]})
    g = build_group_graph(df)
    check(3 in g.nodes, "the singleton is kept as a node")
    check(g.degree(3) == 0, "and has no edges")


def test_centrality_survives_an_isolate():
    """eigenvector_centrality raises on a graph with an isolated node; the
    per-component version does not. This is the shape a real survey produces."""
    df = pd.DataFrame({"id": [1, 2, 3], "peer_group_id": [1, 1, 9]})
    tab = centrality_table(build_group_graph(df))
    check(len(tab) == 3, "one row per node")
    check(tab.loc[tab.id == 3, "eigenvector_centrality"].iloc[0] == 0.0,
          "an isolate scores zero rather than raising")


def test_centrality_is_constant_within_a_clique():
    """The honest limitation, asserted so nobody quotes it as individual influence."""
    out = attach_centrality(sample())
    for _, part in out.groupby("peer_group_id"):
        check(part["degree_centrality"].nunique() == 1,
              "degree is identical within a group, because the graph assumes it")


def test_attach_centrality_does_not_change_the_row_count():
    df = sample()
    check(len(attach_centrality(df)) == len(df), "no rows gained or lost")


def test_duplicate_ids_are_caught_rather_than_multiplying_rows():
    df = pd.DataFrame({"id": [1, 1, 2], "peer_group_id": [1, 1, 1]})
    try:
        attach_centrality(df)
    except ValueError as exc:
        check("duplicates" in str(exc), "the error names the cause")
        return
    raise AssertionError("a duplicate id should not pass silently")


# ------------------------------------------------------------ peer effects ---

def test_leave_one_out_excludes_the_member_and_matches_the_slow_form():
    df = pd.DataFrame({"id": [1, 2, 3, 4], "g": [1, 1, 1, 2],
                       "y": [10.0, 20.0, 30.0, 5.0]})
    got = leave_one_out_mean(df, "y", "g")
    check(got.iloc[0] == 25.0, "(20 + 30) / 2")
    check(got.iloc[1] == 20.0, "(10 + 30) / 2")
    check(np.isnan(got.iloc[3]), "a member alone in a group has no peer mean")

    # the closed form must equal the row-by-row filter it replaced
    slow = df.apply(
        lambda row: df[(df.g == row.g) & (df.id != row.id)]["y"].mean(), axis=1)
    check(np.allclose(got.dropna(), slow.dropna()), "closed form matches the slow one")


def test_including_your_own_value_would_manufacture_the_finding():
    """The error the previous version made, shown rather than described.

    Regressing y on the group mean *including* y gives a large positive
    coefficient on data with no peer structure at all, because the regressor
    contains the dependent variable."""
    rng = np.random.default_rng(0)
    n = 200
    df = pd.DataFrame({"id": range(n), "g": rng.integers(0, 20, n),
                       "y": rng.normal(100, 20, n),
                       "age": rng.normal(40, 8, n),
                       "education_years": rng.integers(0, 13, n),
                       "village": rng.choice(list("ABC"), n)})

    import statsmodels.api as sm
    with_self = df.groupby("g")["y"].transform("mean")
    naive = sm.OLS(df["y"], sm.add_constant(with_self.to_frame("peer"))).fit()
    check(naive.params["peer"] > 0.5,
          "the with-self version finds a large effect in pure noise")

    honest = peer_association(df, outcome="y", group="g", village="village")
    check(abs(honest["coefficient"]) < abs(naive.params["peer"]),
          "the leave-one-out version does not")
    check(honest["p_value"] > 0.01, "and does not call noise significant")


def test_the_result_carries_its_caveat():
    out = peer_association(attach_centrality(sample()))
    check("association" in out["interpretation"].lower(), "labelled an association")
    check("Manski" in out["interpretation"], "and names the identification problem")
    check(out["std_errors"].startswith("clustered"), "standard errors are clustered")


def test_singletons_are_dropped_and_counted():
    rng = np.random.default_rng(1)
    n = 60
    df = pd.DataFrame({"id": range(n),
                       "g": list(rng.integers(0, 10, n - 3)) + [900, 901, 902],
                       "y": rng.normal(100, 20, n),
                       "age": rng.normal(40, 8, n),
                       "education_years": rng.integers(0, 13, n),
                       "village": rng.choice(list("AB"), n)})
    out = peer_association(df, outcome="y", group="g", village="village")
    check(out["dropped_singletons"] >= 3, "the three singletons are dropped")
    check(out["n"] == len(df) - out["dropped_singletons"], "and counted")


# --------------------------------------------------------------- diffusion ---

def test_diffusion_is_reproducible():
    """The previous version used random.choice with no seed, so two runs of the
    same script gave different answers and neither could be checked."""
    g = build_group_graph(sample())
    a = compare_strategies(g, k=5, threshold=0.3, seed=1)
    b = compare_strategies(g, k=5, threshold=0.3, seed=1)
    check(a.equals(b), "same seed, same answer")


def test_a_cascade_cannot_leave_its_component():
    df = pd.DataFrame({"id": range(1, 11), "peer_group_id": [1] * 5 + [2] * 5})
    g = build_group_graph(df)
    run = simulate_diffusion(g, seeds=[1, 2], threshold=0.3)
    check(run["adopters"] <= {1, 2, 3, 4, 5}, "nothing crosses into the other group")


def test_a_threshold_that_is_met_takes_the_whole_clique():
    df = pd.DataFrame({"id": range(1, 6), "peer_group_id": [1] * 5})
    g = build_group_graph(df)
    # each node has 4 neighbours; 2 seeds means 2/4 = 0.5 >= 0.3
    run = simulate_diffusion(g, seeds=[1, 2], threshold=0.3)
    check(run["n_adopters"] == 5, "the whole clique adopts")
    run_high = simulate_diffusion(g, seeds=[1, 2], threshold=0.9)
    check(run_high["n_adopters"] == 2, "and nothing does at a high threshold")


def test_a_per_node_threshold_is_honoured():
    """Two reluctant members in a clique of five, seeded at node 1.

    Nodes 2 and 3 adopt on 1/4 of their neighbours. Nodes 4 and 5 then see 3/4,
    which clears neither 0.99 nor 1.0, and the cascade stops at three. Note that
    a single reluctant node would not hold out: once its four neighbours have
    all adopted it sees 4/4, which meets even a 0.99 threshold. It takes two of
    them refusing together to stall each other."""
    df = pd.DataFrame({"id": range(1, 6), "peer_group_id": [1] * 5})
    g = build_group_graph(df)
    thresholds = {1: 0.1, 2: 0.1, 3: 0.1, 4: 0.99, 5: 1.0}
    run = simulate_diffusion(g, seeds=[1], threshold=thresholds)
    check(run["adopters"] == {1, 2, 3}, "the willing members adopt")
    check(4 not in run["adopters"] and 5 not in run["adopters"],
          "the reluctant ones do not")


def test_an_isolate_never_adopts_unless_seeded():
    df = pd.DataFrame({"id": [1, 2, 3], "peer_group_id": [1, 1, 9]})
    g = build_group_graph(df)
    run = simulate_diffusion(g, seeds=[1], threshold=0.3)
    check(3 not in run["adopters"], "no neighbours, no adoption")


def test_bad_input_is_refused():
    g = build_group_graph(pd.DataFrame({"id": [1, 2], "peer_group_id": [1, 1]}))
    for call, expect in ((lambda: simulate_diffusion(g, seeds=[99]), "not in the graph"),
                         (lambda: simulate_diffusion(g, seeds=[1], threshold=0), "in (0, 1]"),
                         (lambda: seed_strategies(g, k=0), "between 1")):
        try:
            call()
        except ValueError as exc:
            check(expect in str(exc), f"the error explains: {expect}")
        else:
            raise AssertionError(f"expected a refusal mentioning {expect}")


def test_strategies_all_return_the_requested_budget():
    g = build_group_graph(sample())
    for name, seeds in seed_strategies(g, k=5, seed=3).items():
        check(len(seeds) == len(set(seeds)) == 5, f"{name} returns 5 distinct seeds")


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in tests:
        fn()
        print(f"  ok  {fn.__name__}")
    print(f"\n{len(tests)} tests, {PASSED} checks, all passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
