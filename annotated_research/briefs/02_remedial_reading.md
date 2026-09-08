# Brief 2: Remedial reading camps in matched government primary schools

*Illustrative. The programme, the district and every number are invented for
teaching. Annotations in blockquotes use the tags in `../annotation_scheme.md`.*

---

## Summary

A 60-day remedial reading camp was run in 30 government primary schools in a
district of central India, targeting children in classes 3 to 5 who could not
read a class 2 paragraph. Thirty comparison schools were matched on
enrolment, distance to block headquarters and baseline reading level. Using a
difference-in-differences design, the camp raised the share of children able
to read a paragraph by 18 percentage points relative to comparison schools.

> **[FRAME]** The question is clear and matches the title. The outcome is the
> outcome the programme targets. This is a well-framed brief.

> **[DESIGN]** Difference-in-differences with matched comparison schools. This
> can support a causal claim *if* treated and comparison schools would have
> moved in parallel without the programme. That assumption is the whole
> argument, and the reader's job is to look for evidence on it.

## Design and data

Programme schools were selected by the implementing organisation from
among schools where the head teacher agreed to host a camp. Comparison
schools were then selected from the remaining schools in the same blocks,
matched on total enrolment, distance to block headquarters, and the share of
children reading at paragraph level at baseline. Reading was assessed by
trained assessors using a standard graded tool at baseline (June) and
endline (September).

> **[SAMPLE]** "Where the head teacher agreed." Programme schools are schools
> with a willing head teacher; comparison schools are, by construction, mostly
> schools without one. A willing head teacher is also the head teacher whose
> school would have improved more anyway. Matching on enrolment, distance and
> baseline reading does nothing about this, because willingness is not one of
> the matched variables and cannot be. This is selection on the thing that
> matters most, and it biases the estimate upward.

> **[MEASURE]** Independent trained assessors using a graded tool, at both
> rounds, in both arms. This is the right way to measure reading and it is a
> strength of the study. Note it, because the next brief in this set does not
> do it.

## Baseline balance

| | Programme (n=30) | Comparison (n=30) |
|---|---|---|
| Enrolment, classes 3-5 | 84 | 81 |
| Distance to block HQ (km) | 11.2 | 11.9 |
| Reading at paragraph level, baseline | 31% | 29% |
| Reading at paragraph level, previous year (from school records) | 22% | 26% |
| Teachers present on visit day | 2.4 | 1.9 |

> **[DESIGN]** Look at the fourth row. A year before baseline, programme
> schools were three points *behind* comparison schools; at baseline they are
> two points ahead. Programme schools were already improving faster before
> the programme began. That is the parallel-trends assumption failing in the
> table that is supposed to support it. The brief presents this row without
> comment.

> **[SAMPLE]** Teachers present: 2.4 against 1.9. Half a teacher more per
> school is a large difference in a primary school, and it is the kind of
> difference a willing head teacher produces. It was not matched on, and it
> is a plausible reason the programme schools were improving faster anyway.

## Results

| | Programme | Comparison | Difference |
|---|---|---|---|
| Baseline, reading at paragraph level | 31% | 29% | +2 |
| Endline, reading at paragraph level | 58% | 38% | +20 |
| Difference-in-differences | | | **+18 pp** (SE 4.1, clustered by school) |

> **[ANALYSIS]** Standard errors clustered by school, with 60 clusters. This is
> correct for the design and the brief says so. The arithmetic is right; the
> problem is upstream of it.

> **[ANALYSIS]** Nine points of the comparison group's improvement (29 to 38)
> happened with no programme, over a monsoon term. That is the counterfactual
> doing its job. Now apply the pre-trend: programme schools were gaining
> roughly five points a year faster than comparison schools before anything
> happened. Over one term that is on the order of two to three points of the
> eighteen. The corrected estimate is still large. It is smaller than the
> headline, and a brief that had done this arithmetic would be more credible,
> not less.

## Limitations

The comparison schools were not randomly assigned, and programme schools
were selected in part on head teacher willingness, which may be correlated
with unobserved school quality. Pre-programme trends in reading differed
between the two groups. The estimate should therefore be read as an upper
bound.

> **[LIMIT]** This is what a limitations section is for. It names the actual
> weakness, says which direction it biases, and tells the reader how to use
> the number. It is also in tension with the summary, which said "raised by
> 18 points" with no such qualification. The person who wrote this paragraph
> and the person who wrote the summary should talk.

## Conclusion

Sixty-day reading camps produced a substantial improvement in reading
outcomes relative to comparison schools. Given the selection into the
programme, the true effect is likely smaller than 18 points but remains
educationally meaningful. A randomised evaluation at the next phase would
resolve the remaining uncertainty.

> **[CLAIM]** "Produced ... relative to comparison schools" is defensible for
> a difference-in-differences, and the sentence after it does the honest
> discounting. This is a brief whose body is better than its summary; the
> lesson is that most readers only read the summary.

> **[ETHICS]** Children in comparison schools who could not read a paragraph
> were identified by the baseline assessment and then received nothing for a
> term while the evaluation ran. The brief does not say whether they were
> offered the camp afterwards. A design that withholds a remedial programme
> from children known to need it owes them a sentence.

---

*What the annotated reader takes away: a good design does not repair a bad
selection rule. The baseline table contained the evidence against the
identifying assumption, and the brief printed it without reading it.*
