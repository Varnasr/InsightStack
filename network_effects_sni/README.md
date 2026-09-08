# network_effects_sni

Social network analysis on self-help group and village data: who is
connected to whom, whether outcomes move together within a group, and how
far a practice spreads from a set of seeds.

```bash
python -m network_effects_sni.demo                    # the whole chain
python -m network_effects_sni.test_network_effects    # 17 tests, 40 checks
```

Needs `networkx`, `pandas`, `numpy`, `statsmodels`, `scipy`.

## Modules

`network.py` builds the graph and measures position. `attach_centrality`
returns degree, betweenness and eigenvector centrality merged onto the frame.

`peer_effects.py` tests whether a member's savings move with her peers'.
`peer_association` uses leave-one-out peer means, clusters standard errors on
the group, and can absorb village fixed effects.

`diffusion.py` runs a linear threshold cascade. `compare_strategies` gives
the same seeding budget to random, degree, betweenness and one-per-group
seeding and reports the reach of each.

## Limits

Centrality on this data is group size. The graph assumes every member of a
group is connected to every other, so within a group all members have the
same degree and eigenvector centrality. To measure individual position, the
instrument has to ask who each member goes to for advice.

The peer regression is an association. A positive coefficient is consistent
with members responding to each other's behaviour, responding to each other's
characteristics, or sharing a village, a bank and a rainfall shock (Manski
1993). Leave-one-out means remove the mechanical part of the problem, not the
identification part. Identification needs exogenous variation in group
membership, such as randomised assignment or the network structure Bramoullé,
Djebbari and Fortin (2009) use. `peer_association` returns an
`interpretation` string saying this and `print_result` prints it.

A cascade cannot leave the component it starts in. On this data the five
groups have no edges between them, so no seeding strategy reaches a group it
did not seed.

## The demo

With five seeds and a 0.3 threshold, five seeds in the largest group (fifteen
members) reach the whole group, because a third of it clears the threshold.
One seed per group reaches nobody beyond the seeds, because a fifth of a
five-member group does not. The ranking of strategies depends on the
threshold; run it with your own.

## Sources

Manski, "Identification of endogenous social effects: the reflection
problem", *Review of Economic Studies* 60(3), 1993, 531-542.

Bramoullé, Djebbari and Fortin, "Identification of peer effects through
social networks", *Journal of Econometrics* 150(1), 2009, 41-55.

Granovetter, "Threshold models of collective behavior", *American Journal of
Sociology* 83(6), 1978, 1420-1443.
