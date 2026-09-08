# MEL framework: an outline with the questions each section has to answer

A monitoring, evaluation and learning framework is the document that says how
the programme will know whether it is working, and what it will do about it.
`mel_framework_mhh_program.pdf` is a completed example; this is the structure,
with what a reviewer checks in each section.

## 1. Programme summary and theory of change

Half a page. What the programme does, for whom, and the causal chain from
activities to outcome with the assumptions stated. If the theory of change is
a diagram elsewhere, the sentence version goes here anyway.

*Reviewer's check:* can the outcome be reached from the activities by the
stated assumptions, or is there a step the diagram skips?

## 2. Evaluation questions

Three to five, ranked. "Did the programme increase product use among girls in
programme schools?" is a question. "Assess impact" is not. Each question
names its outcome and its comparison.

*Reviewer's check:* does each question have a design in section 4 that can
answer it? A question with no design is a hope.

## 3. Indicators

The logframe's indicator column, each with a reference sheet
(`indicator_reference_sheet.md`). Say which are for monitoring (frequent,
from programme records, about delivery) and which for evaluation (baseline
and endline, from surveys, about change).

*Reviewer's check:* is there at least one outcome indicator that is not
self-reported to programme staff?

## 4. Evaluation design

For each evaluation question: the comparison that will be made, why it
supports the claim the question makes, and its known weaknesses. Before-
after, with-without, difference-in-differences, randomised, regression
discontinuity: name it, and name what it cannot rule out. The annotated
briefs in `../annotated_research/` are five worked examples of what each
design can and cannot claim.

*Reviewer's check:* if the design has no comparison group, does the
framework say so in this section, or only in a limitations paragraph at the
end of the final report?

## 5. Data collection

Instruments, samples, timing, who collects, how quality is checked in the
field. Sample size with the calculation shown, not asserted. FieldStack's
`survey_tools/sample_size_calculator.R` does the calculation and
`field_ops/` does the field checks.

*Reviewer's check:* is the sample size justified for the outcome indicator's
expected change, with the clustering accounted for? A sample sized for a
simple random draw and collected by village is half the size it claims.

## 6. Analysis plan

Written before the data arrive. For each evaluation question: the estimator,
the standard errors (clustered at the level of assignment), the
disaggregations that will be reported, how attrition and missing data will be
handled. A pre-specified analysis plan is what separates a finding from a
search.

*Reviewer's check:* does it say what will be done if attrition differs by
arm? If not, the answer at the time will be "nothing".

## 7. Learning and use

Who receives which result, when, in what form, and what decision it feeds.
"Quarterly review meeting, programme manager, one-page dashboard, decides
whether to reallocate sessions across schools" is a use. "Findings will be
disseminated" is not. `../learning_layers/` is about this section.

*Reviewer's check:* is there a decision named that a result could change? If
every decision is already made, the MEL system is documentation.

## 8. Ethics and data protection

Consent, for adults and for minors with guardians. What happens to the
comparison group. Where identifiable data are stored, who can see them, when
they are deleted. Whether anyone can be identified from a reported
disaggregation (a table with one girl in a cell identifies her).

*Reviewer's check:* is there an approval named, and a person responsible?

## 9. Budget and schedule

Every survey in section 5 with a cost and a month. Every analysis in section
6 with the person who will do it.

*Reviewer's check:* does the endline survey have a budget line? Frameworks
routinely promise an endline nobody has funded.
