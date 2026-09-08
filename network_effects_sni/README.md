# network_effects_sni

Social network analysis on self-help group and village data: who is connected to
whom, whether outcomes co-move within a group, and how far a practice would
spread from a given set of seeds.

```bash
python -m network_effects_sni.demo                    # the whole chain
python -m network_effects_sni.test_network_effects    # 17 tests, 40 checks
```

Needs `networkx`, `pandas`, `numpy`, `statsmodels`, `scipy`.

## Three steps

**`network.py`** builds the graph and measures position. `attach_centrality`
returns degree, betweenness and eigenvector centrality merged back onto the
frame.

**`peer_effects.py`** asks whether a member's savings move with her peers'.
`peer_association` uses leave-one-out peer means, clusters standard errors on
the group, and optionally absorbs village fixed effects.

**`diffusion.py`** runs a linear threshold cascade. `compare_strategies` puts
the same seeding budget behind random, degree, betweenness and one-per-group and
reports how far each gets.

## Three things this will not tell you

**Centrality here is group size wearing a different name.** The graph is built by
assuming everyone in a self-help group is connected to everyone else in it, so
within a group every member has identical degree and identical eigenvector
centrality. All the variation across the sample is variation in how big the
groups are. A test asserts this rather than leaving it to be discovered.

To measure individual position you need the instrument to ask who each member
actually goes to for advice. That gives a directed graph with real within-group
variation, and then centrality means what people assume it means.

**The peer regression is an association and cannot be more.** Manski's reflection
problem: a positive coefficient is consistent with three different worlds and the
data cannot separate them. Members may respond to each other's behaviour
(the thing you want), or to each other's characteristics, or they may simply
share a village, a bank, a rainfall shock, and the fact that they chose each
other in the first place. Leave-one-out means remove the mechanical part of the
problem and leave the identification part exactly where it was.

What would identify it is exogenous variation in who is grouped with whom:
randomised assignment, or the intransitive network structure Bramoullé,
Djebbari and Fortin (2009) exploit, where a friend's friend who is not your
friend supplies the instrument. Fully connected groups have no such structure.
`peer_association` returns an `interpretation` string saying so, and
`print_result` prints it under every estimate.

**A cascade cannot leave the component it starts in.** On this data the five
groups have no edges between them, so no seeding strategy reaches a group it did
not seed. That is worth seeing, because it says the binding constraint is the
network rather than the targeting rule.

## What the demo shows, and why it is counterintuitive

With five seeds and a 0.3 threshold, concentrating all five in the largest group
reaches fifteen members. Spreading one per group reaches five, which is to say
nobody beyond the women who were trained.

The reason is arithmetic on the threshold, not anything about centrality. Five
seeds in a group of fifteen is a third of it, which clears 0.3 and takes the
whole group. One seed in a group of five is a fifth, clears nothing, and stops.
Change the threshold and the ranking changes with it. This is why the model is
worth running with your own threshold rather than quoting a rule of thumb about
targeting central nodes.

## What this replaced

Four scripts that could not run as a chain. `sni_analysis.py` wrote its plot to
a `visualizations/` directory that does not exist in the repository, so it
raised `FileNotFoundError` after doing all the work. `calculate_sni.py`
duplicated most of it under different column names and wrote a file nothing
read. `peer_effects_regression.py` opened a CSV under a path neither script
wrote. `diffusion_model.py` picked its seed with `random.choice` and no seed
set, so two runs gave different answers and neither could be checked.

The peer regression also computed a group mean *including* the member's own
savings, on the line above the leave-one-out version, and left both in the
frame. `test_including_your_own_value_would_manufacture_the_finding` shows what
that costs: on pure noise with no peer structure at all, the with-self version
returns a large positive coefficient, because the regressor contains the
dependent variable.

## Sources

Manski, "Identification of endogenous social effects: the reflection problem",
*Review of Economic Studies* 60(3), 1993, 531-542.

Bramoullé, Djebbari and Fortin, "Identification of peer effects through social
networks", *Journal of Econometrics* 150(1), 2009, 41-55.

Granovetter, "Threshold models of collective behavior", *American Journal of
Sociology* 83(6), 1978, 1420-1443.
