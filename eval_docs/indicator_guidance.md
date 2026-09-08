# Choosing indicators, and the errors that make them useless

An indicator is a number that will be quoted without its context. Choose it
knowing that.

## Five tests, in the order to apply them

**1. Does it measure the objective, or something near it?** "Number of health
sessions held" is near "girls know about menstrual hygiene" and is not it.
Sessions held is an output; knowledge is an outcome; practice is a further
outcome; the objective decides which is wanted. The most common indicator
error is measuring the thing that is easy to count and placing it in the row
of the thing that is hard to.

**2. Can the denominator be stated in one sentence?** If not, the indicator
cannot be computed the same way twice. See `indicator_reference_sheet.md`.

**3. Will it move in the time available, by enough to see?** A stunting rate
moves a point or two a year with everything going right. A programme
measured on it over eighteen months will show nothing whatever it did.
Choose an indicator on the causal path that responds faster: feeding
practice, dietary diversity, or, if the programme is about it, weight-for-age
in the specific cohort reached.

**4. Can it be gamed by the people who report it?** Attendance registers
filled in by teachers whose school is being evaluated on attendance. Session
counts reported by the staff whose job depends on session counts. Where the
reporter has a stake, the indicator needs an independent check or a
different source, and the sheet should say which.

**5. Is it worth what it costs to collect?** An anthropometric survey of two
thousand children costs what three field staff cost for a year. A
programme with eight outcome indicators each needing its own survey has
chosen not to collect any of them properly.

## Types, and what each is for

| Type | Example | Use it for |
|---|---|---|
| Count | Peer leaders trained | Outputs. Never as an outcome |
| Coverage | Share of target schools with an active club | Outputs where reach matters more than volume |
| Prevalence | Share of girls using a product | Outcomes. Needs a clean denominator |
| Mean | Mean days absent per girl per month | Outcomes where the distribution matters, and report the distribution too |
| Index | Composite hygiene practice score | Only when the components would be reported separately anyway and a summary is wanted on top. See EquityStack `social_sector/composite_index.py` for what an index has to decide |
| Rate | Deaths per thousand births | Goal-level, from sources you do not control |

## Errors that recur

**Percentages of small denominators.** "75 per cent of peer leaders" is three
of four. Report the count when the base is under fifty.

**Self-reported behaviour, collected by the programme, after the programme
taught the right answer.** The indicator measures what respondents learned to
say. Prefer observed behaviour, records the respondent did not produce, or
an enumerator the respondent does not associate with the programme.

**A target set from the baseline plus a round number.** Targets should come
from what comparable programmes achieved, and the sheet should cite one.
Where none exists, say the target is a guess.

**Changing the definition between rounds.** Adding a product to the list of
"sanitary products" at endline raises the indicator without anything having
changed. Freeze the definition at baseline; if it must change, report both.

**Reporting an outcome only for participants.** Share of *participating*
girls using a product is a different indicator from share of *all* girls in
the target schools, and the first is always higher. The logframe says which
was promised.
