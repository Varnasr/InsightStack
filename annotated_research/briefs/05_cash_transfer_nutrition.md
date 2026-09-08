# Brief 5: Maternity cash transfer and child weight, at an eligibility cutoff

*Illustrative. The programme, the state and every number are invented for
teaching. Annotations in blockquotes use the tags in `../annotation_scheme.md`.*

---

## Summary

A state maternity benefit paid ₹6,000 in three instalments to women in
households scoring below 32 on a 100-point deprivation index. Using
administrative data on 41,000 births and the anthropometric records from the
first-year immunisation visit, a regression discontinuity design at the
cutoff finds that the transfer raised weight-for-age at twelve months by
0.14 standard deviations among children of eligible mothers. The transfer
improves child nutrition and the eligibility threshold should be raised.

> **[FRAME]** Question and outcome agree. Weight-for-age at twelve months is
> an appropriate, objectively measured nutrition outcome for a transfer paid
> during pregnancy and infancy.

> **[DESIGN]** Regression discontinuity at an administrative cutoff. Where the
> score cannot be manipulated and nothing else changes at 32, households just
> below and just above are as good as randomly assigned, and the design
> supports a causal claim *for households near the cutoff*. That last clause
> is the one the summary's final sentence forgets.

## Design and data

The deprivation index is computed by the state from household census data
collected in 2021 and is not visible to households. Eligibility is
determined by the score at the time of the birth registration. Birth
records for 2023 were linked to the immunisation register, which records
weight at the 9-to-12-month visit, by the mother's identifier. Of 41,200
births, 36,850 (89 per cent) were linked to a weight record. The analysis
uses births to mothers with index scores between 20 and 44, a bandwidth of
12 points either side of the cutoff (n = 14,300), with local linear
regression and triangular weights.

> **[DESIGN]** Score computed from prior census data, invisible to households,
> fixed before the birth. That closes the usual manipulation channel: a
> household cannot choose to sit just below 32. The brief should show a
> density plot of the score around the cutoff, which is the standard
> evidence that nobody bunched, and it does not. The claim is plausible; the
> figure is missing.

> **[SAMPLE]** 89 per cent linked to a weight record, and the question is
> whether linkage differs across the cutoff. Eligible mothers receive the
> third instalment on completing immunisation, so they have a reason to
> attend the visit at which weight is recorded; ineligible mothers do not.
> If attendance jumps at the cutoff, so does the probability of having an
> outcome at all, and the children with a weight record just above 32 are a
> different selection from those just below. This is the study's main
> threat and it is checkable from the same data.

> **[MEASURE]** Weight recorded by an auxiliary nurse-midwife at a routine
> visit, on whatever scale the sub-centre has, with the child's age from the
> birth record. Objective, not self-reported, and measured identically on
> both sides of the cutoff. Measurement error here adds noise and does not
> bias the discontinuity. This is the right kind of outcome.

## Results

| | Estimate | SE | Bandwidth |
|---|---|---|---|
| Weight-for-age z at 12 months, at the cutoff | +0.14 | 0.05 | 12 |
| Same, bandwidth 8 | +0.16 | 0.07 | 8 |
| Same, bandwidth 16 | +0.12 | 0.04 | 16 |
| Probability of a linked weight record, at the cutoff | +0.06 | 0.01 | 12 |
| Mother's age at birth, at the cutoff (placebo) | +0.1 | 0.2 | 12 |
| Birth order, at the cutoff (placebo) | -0.02 | 0.04 | 12 |

> **[ANALYSIS]** Three bandwidths, two placebo outcomes that do not jump, and
> the estimate is stable across bandwidths. This is how a regression
> discontinuity should be reported, and it is done here.

> **[ANALYSIS]** The fourth row is the important one and the brief reports it
> without discussing it. The probability of having an outcome jumps six
> points at the cutoff. The children who newly appear in the data on the
> eligible side are children whose mothers attended because of the
> transfer's incentive; if those are healthier-than-average children of
> more-engaged mothers, part of the 0.14 is composition. The standard
> response is to bound the effect under assumptions about the six per cent,
> and it is not done.

## Limitations

The estimate is local to households near the cutoff and may not apply to
households far below it. The data cover one year of births.

> **[LIMIT]** The first sentence is the right limitation, stated correctly.
> The second is fine. The missing one is the differential linkage the
> brief's own table shows.

## Conclusion

The transfer improves infant nutrition. Raising the eligibility threshold
from 32 to 40 would extend the benefit to an additional 120,000 births per
year at a cost of ₹72 crore.

> **[CLAIM]** "Improves infant nutrition" is supported for children of
> mothers scoring near 32, subject to the linkage question. The
> recommendation then takes a local estimate and applies it to households
> scoring 32 to 40, who are less deprived than the households the estimate
> is about. A cash transfer's effect on nutrition is plausibly *smaller* for
> less deprived households, so the extension would likely buy less than 0.14
> per child. That is not an argument against extending it; it is an argument
> that the cost per unit of effect in the recommendation is understated, and
> the brief's own limitations section already said so.

> **[ETHICS]** Administrative data linked on the mother's identifier, at
> household level, with a deprivation score. The brief should state who
> approved the linkage, whether the analysis dataset was de-identified, and
> where it is held. Individual-level linked welfare and health records are
> the most sensitive data a state holds about a household.

---

*What the annotated reader takes away: this is the strongest design in the
set, reported mostly well, and it still has one uncorrected threat visible in
its own table and one recommendation that reaches past what the design
identifies. Good studies are the ones where the remaining problems are
specific.*
