"""Build the peer network from self-help group membership, and measure position.

One module rather than the two near-duplicate scripts that were here, which
computed overlapping centrality measures under different column names, wrote to
two different files, and disagreed about which one the regression should read.

The graph is constructed by assuming everyone in a self-help group is connected
to everyone else in it. That is an assumption about the data, not a fact about
the world, and it has a consequence worth being clear about before any of these
numbers are interpreted: within a clique, every member has identical degree and
near-identical eigenvector centrality. Variation in centrality across the sample
is therefore variation in *group size*, not in individual popularity.

Real influence data means naming names. Where the survey asks "who in this group
do you go to for advice", the resulting directed graph has genuine within-group
variation and centrality means what people think it means. Where it does not,
say what you have: a group-size measure.
"""

from __future__ import annotations

from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd

__all__ = ["build_group_graph", "centrality_table", "attach_centrality"]

DATA = Path(__file__).resolve().parent / "data"


def build_group_graph(df: pd.DataFrame, *, id_col: str = "id",
                      group_col: str = "peer_group_id") -> nx.Graph:
    """One undirected clique per group, all groups in one graph.

    Isolated members (a group of one) are added as nodes with no edges rather
    than dropped, so the node set matches the sample and a later merge does not
    lose rows silently.
    """
    for col in (id_col, group_col):
        if col not in df.columns:
            raise KeyError(f"build_group_graph: no column {col!r} in the frame")

    g = nx.Graph()
    g.add_nodes_from(df[id_col].tolist())
    for _, members in df.groupby(group_col)[id_col]:
        ids = members.tolist()
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                g.add_edge(ids[i], ids[j])
    return g


def centrality_table(g: nx.Graph, *, id_col: str = "id") -> pd.DataFrame:
    """Degree, betweenness and eigenvector centrality, one row per node.

    Eigenvector centrality needs care on this graph shape and gets it here.

    It is undefined across a disconnected graph, so it is computed per connected
    component. Isolates get 0. And it is computed by a dense symmetric solve
    rather than through networkx, because both networkx routes fail on the
    components a survey of small groups actually produces:
    `eigenvector_centrality` raises `PowerIterationFailedConvergence`, and
    `eigenvector_centrality_numpy` goes through ARPACK, which refuses a
    component of two nodes with "Cannot use scipy.linalg.eig for sparse A with
    k >= N - 1". A group of two members is ordinary.

    Normalised to unit L2 norm, matching networkx, so a clique of *n* members
    each scores 1/sqrt(n).
    """
    if g.number_of_nodes() == 0:
        raise ValueError("centrality_table: the graph has no nodes")

    degree = nx.degree_centrality(g)
    betweenness = nx.betweenness_centrality(g)

    eigen: dict = {}
    for component in nx.connected_components(g):
        sub = g.subgraph(component)
        if sub.number_of_edges() == 0:
            eigen.update({n: 0.0 for n in sub.nodes})
            continue
        nodes = list(sub.nodes)
        adjacency = nx.to_numpy_array(sub, nodelist=nodes)
        values, vectors = np.linalg.eigh(adjacency)
        principal = np.abs(vectors[:, int(np.argmax(values))])
        norm = np.linalg.norm(principal)
        if norm > 0:
            principal = principal / norm
        eigen.update(dict(zip(nodes, principal.tolist())))

    return pd.DataFrame({
        id_col: list(g.nodes),
        "degree_centrality": [degree[n] for n in g.nodes],
        "betweenness_centrality": [betweenness[n] for n in g.nodes],
        "eigenvector_centrality": [eigen[n] for n in g.nodes],
        "group_size": [g.degree(n) + 1 for n in g.nodes],
    })


def attach_centrality(df: pd.DataFrame, *, id_col: str = "id",
                      group_col: str = "peer_group_id") -> pd.DataFrame:
    """Convenience: build the graph and merge the measures back on.

    Raises on a duplicated id before merging, and again if the merge changed the
    row count. The duplicate check has to come first: two rows sharing an id
    collapse into one graph node, so the merge returns the original row count
    and looks fine while quietly giving both rows the same network position.
    """
    if df[id_col].duplicated().any():
        offenders = df.loc[df[id_col].duplicated(keep=False), id_col].unique()
        raise ValueError(
            f"attach_centrality: {id_col!r} has duplicates ({list(offenders)[:5]}). "
            "Two rows sharing an id become one node, so both would silently get "
            "the same network position.")

    g = build_group_graph(df, id_col=id_col, group_col=group_col)
    out = df.merge(centrality_table(g, id_col=id_col), on=id_col, how="left")
    if len(out) != len(df):
        raise ValueError(
            f"attach_centrality: the merge changed the row count from {len(df)} to "
            f"{len(out)}")
    if out["degree_centrality"].isna().any():
        raise ValueError("attach_centrality: some rows got no centrality measure")
    return out
