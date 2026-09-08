# Brief 4: Financial literacy for self-help groups, randomised by village

*Illustrative. The programme, the district and every number are invented for
teaching. Annotations in blockquotes use the tags in `../annotation_scheme.md`.*

---

## Summary

A six-module financial literacy curriculum was delivered to women's
self-help groups in 80 villages randomly selected from 160 in two blocks of a
southern state, with the other 80 serving as controls. Twelve months after
the programme, treated women reported monthly savings 31 per cent higher than
control women (₹412 against ₹314) and were 14 percentage points more likely
to hold an individual bank account. The curriculum caused a substantial and
significant increase in savings behaviour.

> **[FRAME]** Question, outcome and title agree. Savings and account
> ownership are what the curriculum is for.

> **[DESIGN]** Randomised at village level, with a control arm. This is the
> design that can support a causal verb, and the brief is entitled to use
> one, subject to what follows.

## Design and data

The 160 villages were stratified by block and by the number of active SHGs,
and 80 were assigned to treatment by lottery in a public draw. All SHG
members in all 160 villages were listed at baseline (n = 4,120 women) and a
random sample of 15 per village was surveyed (n = 2,400). The endline survey
attempted to re-interview the same women (n = 1,986 completed).

> **[SAMPLE]** Public lottery, stratified, baseline listing before assignment.
> This is done properly, and it is rarer than it should be.

> **[SAMPLE]** Endline completed 1,986 of 2,400: 17 per cent attrition
> overall. The number that matters is attrition *by arm*, and it is in the
> next table.

## Baseline balance and attrition

| | Treatment | Control | Difference |
|---|---|---|---|
| Villages | 80 | 80 | |
| Women surveyed at baseline | 1,200 | 1,200 | |
| Monthly savings, baseline (₹) | 288 | 291 | -3 (p=0.84) |
| Holds individual bank account | 41% | 43% | -2 (p=0.51) |
| Years of schooling | 5.1 | 5.0 | +0.1 (p=0.77) |
| **Re-interviewed at endline** | **1,062 (89%)** | **924 (77%)** | **+12 pp (p<0.01)** |

> **[SAMPLE]** Balance at baseline is good, as randomisation should produce.
> Attrition is not balanced: 89 per cent of treated women were found again
> and 77 per cent of control women. Twelve points of differential attrition in
> a savings study is serious. The women who leave an SHG, migrate for work, or
> stop attending are plausibly the women with the least savings. If the
> control arm lost more of them, the control arm's endline mean is inflated
> and the estimated effect is *understated*; if the treatment arm's extra
> retention is the programme keeping low-savers engaged, the treatment mean
> is *deflated*. Either way the 31 per cent is not the number a full sample
> would give, and the brief has to say which way it thinks the bias runs.

> **[MEASURE]** "Reported monthly savings." Self-reported, to an enumerator
> from the organisation that ran the training, twelve months after that
> training told the women that saving is what good members do. This is the
> same problem as Brief 1 and it is not fixed by randomisation: both arms are
> asked the same question, but only one arm has been taught the desirable
> answer. Passbook data from the SHG's own records would measure the same
> thing without the demand effect, and the brief does not say why it was not
> used.

## Results

| Outcome | Treatment | Control | Difference | p |
|---|---|---|---|---|
| Monthly savings (₹) | 412 | 314 | +98 (+31%) | <0.001 |
| Holds individual bank account | 61% | 47% | +14 pp | <0.001 |
| Took a loan from the SHG in last year | 38% | 36% | +2 pp | 0.42 |
| Loan used for income-generating activity | 52% | 49% | +3 pp | 0.55 |

Standard errors are heteroskedasticity-robust. Estimates are from OLS with
block fixed effects.

> **[ANALYSIS]** "Heteroskedasticity-robust" is not the same as clustered.
> Treatment was assigned to villages; women in the same village share the
> assignment and share everything else about the village. The standard errors
> must be clustered at the village, the level of randomisation, with 160
> clusters. Robust-but-unclustered errors on a village-randomised design are
> too small, often by a factor of two or three. The p-values in this table
> are wrong and the direction is known: every one of them is too small.

> **[ANALYSIS]** Nothing is said about how the 414 missing women were handled.
> The honest options are: report the effect under bounding assumptions (Lee
> bounds are the standard), or reweight on baseline characteristics and say
> so. Reporting the complete-case difference as if attrition were random,
> when the table shows it was not, is the choice the brief made.

## Limitations

Savings were self-reported. Attrition was higher in the control group, which
may bias the estimates. The study covered two blocks and may not generalise.

> **[LIMIT]** All three named limitations are real, and the middle one is the
> one that matters. "May bias" is doing a lot of work: the brief has the
> baseline characteristics of the attritors and could say in which direction.
> Not saying is a choice.

## Conclusion

Financial literacy training delivered through SHGs causes a large and
statistically significant increase in savings and formal account ownership,
and should be integrated into the state's SHG programme.

> **[CLAIM]** "Causes" is earned by the design and undermined by the analysis.
> With village-clustered errors the savings result is probably still
> significant and the account result probably is; with a bounding treatment
> of attrition the savings result may not be. "Large" depends on whether the
> ₹98 survives both corrections. The brief should have run them; a reader
> cannot.

> **[ETHICS]** Control villages received nothing for twelve months and the
> brief does not say whether they received the curriculum afterwards. In a
> randomised study where the treatment is training rather than a scarce good,
> delivering it to controls after endline costs little and is the norm.

---

*What the annotated reader takes away: randomisation buys the right to a
causal verb and does not pay for the analysis. Differential attrition and
unclustered errors on a clustered design can each turn a real finding into an
unreliable number, and here both are present.*
