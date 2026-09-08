# The annotation scheme

Every brief in `briefs/` is marked up with the same eight tags. The tags are
the reusable part: apply them to any research note, evaluation summary or
rapid assessment that lands on your desk, and the places where a document is
strong or weak become visible on one reading.

An annotation is a blockquote beginning with the tag in bold:

> **[CLAIM]** The sentence above says "reduced", and the design cannot support
> that verb. "Was lower among" is what the data show.

## The eight tags

| Tag | The question it asks of the text |
|---|---|
| **[FRAME]** | What question is this actually answering, and is it the one the title promises? A brief titled "impact of X" that describes a cross-section is answering a different question from the one it names. |
| **[DESIGN]** | What comparison is being made, and what would have happened without the programme? Before-after, with-without, difference-in-differences, randomised: each supports a different strength of claim, and the design decides the ceiling on what the conclusion can say. |
| **[SAMPLE]** | Who is in the data, how were they chosen, and who is missing? Convenience samples, self-selected participants, and dropouts between rounds each bias in a predictable direction. Say which. |
| **[MEASURE]** | What was actually recorded, by whom, and does it mean what the text says it means? Self-reported attendance, a proxy for consumption, an index whose construction is not shown. |
| **[ANALYSIS]** | Is the arithmetic right for the design? Clustered standard errors on a clustered sample, survey weights where the sample was stratified, a control for something that is itself an outcome. |
| **[LIMIT]** | Does the text name its own weaknesses, and are the named ones the real ones? A limitations paragraph that lists "sample size" and omits "no comparison group" is doing PR, not science. |
| **[CLAIM]** | Does the conclusion's verb match what the design can support? *Associated with*, *higher among*, *increased*, *caused*: these are not synonyms. |
| **[ETHICS]** | Consent, who benefited from participating, what happened to the control group, whether any respondent could be identified from what is reported. |

## How to use it for teaching

Hand out the brief without the annotations first. Have readers mark it up
with the eight tags themselves, then compare against the annotated version.
The disagreements are the lesson: where two readers tag the same sentence
differently, the text is ambiguous, and that ambiguity is usually where a
misleading claim lives.

## The briefs

All five are illustrative. The programmes, districts, organisations and
numbers are invented to make the teaching points, and no brief describes a
real study or cites a real one. Each is written the way such notes are
actually written, which means each contains errors that real notes contain,
and the annotations find them.

| Brief | Sector | Design | The main lesson |
|---|---|---|---|
| `briefs/01_school_health_clubs.md` | Health and education | Before-after, one arm | A before-after comparison during a school year cannot separate the programme from growing up |
| `briefs/02_remedial_reading.md` | Education | Difference-in-differences, matched schools | The parallel-trends assumption is stated and then contradicted by the baseline table |
| `briefs/03_flood_early_warning.md` | Climate | Cross-section after the event | Survivorship in who could be interviewed, and an outcome measured only where the programme ran |
| `briefs/04_shg_savings.md` | Gender and livelihoods | Randomised at village level, with attrition | A good design weakened by differential dropout, and an analysis that ignores the clustering |
| `briefs/05_cash_transfer_nutrition.md` | Livelihoods and nutrition | Regression discontinuity on an eligibility cutoff | A credible design, and a claim that reaches past the population it identifies |

The earlier `annotated_research_brief_mhh.pdf` is the original example and is
kept as it was.
