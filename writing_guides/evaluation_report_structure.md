# Structure of an evaluation report

The reader is a programme manager or a donor officer with twenty minutes.
They will read the summary, look at one table, and skim the recommendations.
Structure the report so that those three things are true on their own and
consistent with everything else.

## The order

**1. Summary (one page).** The evaluation question, the design in one
sentence, the headline result with its uncertainty, the main limitation, and
the recommendation. Every number in the summary appears in a table later with
the same value. The summary's verbs match the design: see "The verb" below.

**2. The programme and the question.** What was done, for whom, where, when.
The evaluation question stated as a question. What would count as the
programme having worked, decided before the data.

**3. Design.** The comparison being made and why it supports the claim. What
it cannot rule out, stated here and not saved for the limitations. The
sample: who, how selected, how many, and how many were lost between rounds,
by arm.

**4. Data.** Instruments, when collected, by whom, how quality was checked.
Attrition and missingness handled explicitly. A table of baseline balance
between arms, including anything that would have predicted the outcome.

**5. Results.** One table per evaluation question, with the estimate, its
standard error or interval, the sample size behind it, and the level at
which errors are clustered. Disaggregations promised in the MEL framework,
each reported whether or not it is interesting. A null result reported in the
same format as a positive one.

**6. Limitations.** The real ones. Ranked by how much they threaten the
headline, with the direction of bias where it is known. A limitations
section that lists "sample size" and "short duration" and omits "no
comparison group" is doing public relations.

**7. Recommendations.** Each one traceable to a specific result. "Scale up"
requires a result that supports scale-up; a before-after study does not
provide one, and the recommendation from a before-after study is "run a
comparison-group study before scaling". Cost per unit of effect where it can
be computed.

**8. Annexes.** Instruments, the analysis plan as pre-specified, the
deviations from it, the full tables, the code or a pointer to it.

## The verb

The single most consequential choice in the report is the verb in the
summary's headline sentence, and it is decided by section 3, not by the size
of the number.

| Design | The verb the summary may use |
|---|---|
| Cross-section, one arm | "was", "reported", "among participants" |
| Before-after, one arm | "rose from X to Y among participants". Never "increased" without "among participants"; never "the programme increased" |
| With-without, not randomised | "was higher in programme areas than comparison areas". "Associated with" |
| Difference-in-differences | "increased relative to comparison areas", with the parallel-trends caveat in the same paragraph |
| Randomised | "increased", "caused", "reduced", subject to attrition and clustering being handled |
| Regression discontinuity | "increased, for households near the threshold" |

The annotated briefs in `../annotated_research/` are five reports read
against this table.

## Things to cut

Background on the sector that the reader knows. A methods section that
explains what a survey is. A findings section organised by instrument rather
than by question. Recommendations that are not connected to a finding.
Anything in the summary that is not in the body.

## Two checks before it goes out

Read only the summary and the tables. Does the summary claim anything the
tables do not show?

Read only the limitations and the recommendations. Does any recommendation
survive its own limitations?
