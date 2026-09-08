"""Social network analysis on self-help group and village diffusion data.

    from network_effects_sni import attach_centrality, peer_association, simulate_diffusion

Three things, in the order you would do them: build the network and measure
position, look at whether outcomes co-move within a group, and simulate how far
a practice would spread from a given set of seeds.

Read `peer_effects.py`'s module docstring before quoting any coefficient from
here. The reflection problem is not a footnote on this kind of regression, it is
the reason the regression cannot answer the question it looks like it answers.
"""

from .network import attach_centrality, build_group_graph, centrality_table
from .peer_effects import leave_one_out_mean, peer_association, print_result
from .diffusion import simulate_diffusion, seed_strategies

__all__ = [
    "attach_centrality", "build_group_graph", "centrality_table",
    "leave_one_out_mean", "peer_association", "print_result",
    "simulate_diffusion", "seed_strategies",
]
