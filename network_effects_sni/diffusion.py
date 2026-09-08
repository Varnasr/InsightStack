"""Threshold diffusion: how far a practice spreads, and where to start it.

A linear threshold model (Granovetter 1978). A member adopts once the share of
her neighbours who have adopted crosses her threshold, and the process runs
until nothing more changes. It answers a question programmes actually ask: given
that we can train twelve women, which twelve maximise how far the practice
travels on its own.

Three things the version this replaces got wrong, all of which matter more than
they look.

**It was not reproducible.** The seed was chosen with `random.choice` and no
seed set, so two runs of the same script gave different answers and neither
could be checked. Every function here takes a `seed`.

**A single random seed node answers nothing.** The interesting comparison is
between *strategies*: random, highest degree, highest betweenness. On a graph
of disconnected cliques, which is what group membership produces, the answer is
stark and worth seeing, since a practice cannot leave the group it starts in
however central the seed.

**A uniform threshold is a strong assumption.** 0.3 for everybody means adoption
depends only on network position. Real heterogeneity in willingness is usually
larger than the network effect, so `threshold` accepts a per-node mapping.
"""

from __future__ import annotations

from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd

__all__ = ["simulate_diffusion", "seed_strategies", "compare_strategies"]

DATA = Path(__file__).resolve().parent / "data"


def simulate_diffusion(g: nx.Graph, seeds, *, threshold=0.3,
                       max_rounds: int = 100) -> dict:
    """Run a linear threshold cascade from ``seeds`` until it stops.

    Parameters
    ----------
    threshold
        A float applied to everyone, or a mapping from node to their own
        threshold. A node with no neighbours never adopts unless seeded, which
        is correct and is why isolate counts matter to the result.
    max_rounds
        A guard. The process is monotone so it always terminates, but a
        malformed threshold (negative, or above 1) would otherwise spin.

    Returns the adopter set, the count per round, and the final share.
    """
    seeds = list(seeds)
    unknown = [s for s in seeds if s not in g]
    if unknown:
        raise ValueError(f"simulate_diffusion: seed(s) not in the graph: {unknown}")
    if isinstance(threshold, (int, float)):
        if not 0 < threshold <= 1:
            raise ValueError("simulate_diffusion: threshold must be in (0, 1]")
        thresholds = {n: float(threshold) for n in g.nodes}
    else:
        missing = [n for n in g.nodes if n not in threshold]
        if missing:
            raise ValueError(
                f"simulate_diffusion: no threshold for {len(missing)} node(s); "
                "supply one per node or pass a single float")
        thresholds = {n: float(threshold[n]) for n in g.nodes}

    adopted = set(seeds)
    per_round = [len(adopted)]
    for _ in range(max_rounds):
        newly = set()
        for node in g.nodes:
            if node in adopted:
                continue
            neighbours = list(g.neighbors(node))
            if not neighbours:
                continue
            share = sum(nb in adopted for nb in neighbours) / len(neighbours)
            if share >= thresholds[node]:
                newly.add(node)
        if not newly:
            break
        adopted |= newly
        per_round.append(len(adopted))

    return {
        "adopters": adopted,
        "n_adopters": len(adopted),
        "share": len(adopted) / g.number_of_nodes(),
        "rounds": len(per_round) - 1,
        "cumulative_by_round": per_round,
        "seeds": seeds,
    }


def seed_strategies(g: nx.Graph, k: int, *, seed: int = 0) -> dict:
    """Three ways of picking ``k`` starting nodes, for comparison.

    ``random`` is the benchmark any targeting rule has to beat. ``degree`` and
    ``betweenness`` are the usual heuristics. On disconnected cliques all three
    perform similarly within a component and none of them can cross between
    components, which is the finding rather than a disappointment.
    """
    if k < 1 or k > g.number_of_nodes():
        raise ValueError(
            f"seed_strategies: k must be between 1 and {g.number_of_nodes()}")
    rng = np.random.default_rng(seed)
    nodes = list(g.nodes)

    by_degree = sorted(nodes, key=lambda n: (-g.degree(n), n))[:k]
    bet = nx.betweenness_centrality(g)
    by_between = sorted(nodes, key=lambda n: (-bet[n], n))[:k]
    # One per component, largest first: the only strategy that can reach a
    # clique nobody is connected to.
    components = sorted(nx.connected_components(g), key=len, reverse=True)
    spread = [sorted(c, key=lambda n: (-g.degree(n), n))[0] for c in components][:k]

    return {
        "random": [nodes[i] for i in rng.choice(len(nodes), size=k, replace=False)],
        "degree": by_degree,
        "betweenness": by_between,
        "one_per_group": spread,
    }


def compare_strategies(g: nx.Graph, k: int, *, threshold=0.3,
                       seed: int = 0) -> pd.DataFrame:
    """Final adoption under each seeding strategy, same budget."""
    rows = []
    for name, seeds in seed_strategies(g, k, seed=seed).items():
        run = simulate_diffusion(g, seeds, threshold=threshold)
        rows.append({"strategy": name, "n_seeds": len(seeds),
                     "n_adopters": run["n_adopters"],
                     "share": round(run["share"], 3),
                     "rounds": run["rounds"]})
    return pd.DataFrame(rows).sort_values("n_adopters", ascending=False)
