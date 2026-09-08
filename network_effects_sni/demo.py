"""Run the whole chain on the bundled sample, and print what it shows.

    python -m network_effects_sni.demo

Three steps: build the network and measure position, look at whether savings
co-move within a group, simulate how far a practice spreads from five seeds.
Everything is seeded, so two runs give the same answer and a change in the
output means a change in the code.
"""

from pathlib import Path

import networkx as nx
import pandas as pd

from .diffusion import compare_strategies
from .network import attach_centrality, build_group_graph
from .peer_effects import peer_association, print_result

DATA = Path(__file__).resolve().parent / "data"


def main() -> None:
    frame = pd.read_csv(DATA / "shg_peer_influence.csv")

    print("=" * 72)
    print("1. Network position")
    print("=" * 72)
    with_centrality = attach_centrality(frame)
    print(with_centrality[["id", "peer_group_id", "group_size",
                           "degree_centrality", "eigenvector_centrality"]]
          .head(8).to_string(index=False))
    print("\nEvery member of a group has the same degree, because the graph was "
          "built by assuming everyone in a group knows everyone else. So "
          "centrality here varies with group size and nothing else. To measure "
          "individual position you need the survey to ask who each member "
          "actually goes to.")

    print("\n" + "=" * 72)
    print("2. Do savings co-move within a group?")
    print("=" * 72)
    print_result(peer_association(with_centrality))

    print("\n" + "=" * 72)
    print("3. Where to put five trainings")
    print("=" * 72)
    graph = build_group_graph(frame)
    print(f"{graph.number_of_nodes()} members in "
          f"{nx.number_connected_components(graph)} groups with no edges between them.\n")
    print(compare_strategies(graph, k=5, threshold=0.3, seed=1).to_string(index=False))
    print("\nConcentrating all five seeds in the largest group wins here, and the "
          "reason is the threshold rather than anything about centrality: five "
          "seeds in a group of fifteen is a third of that group's members, which "
          "clears the 0.3 threshold and takes the whole group. One seed per "
          "group is a fifth or less everywhere, clears nothing, and the practice "
          "never leaves the five women who were trained.")
    print("\nNo strategy reaches a group it did not seed. The graph has no edges "
          "between groups, so a practice cannot travel between them at all, and "
          "no amount of clever targeting changes that. If the programme needs "
          "reach across villages, the network is the thing to change, not the "
          "seeding rule.")


if __name__ == "__main__":
    main()
