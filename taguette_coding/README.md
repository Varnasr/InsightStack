# Qualitative coding with Taguette

One coded focus group discussion, start to finish: the transcript, the tag
file Taguette produced, and the export that goes to analysis. This is the
worked example for the qualitative half of a mixed-methods evaluation, and
the method note that goes with it.

| File | What it is |
|---|---|
| `chhattisgarh_chw_fgd.txt` | A focus group discussion with community health workers, as the transcript Taguette reads. Illustrative, not a real group |
| `chhattisgarh_chw_fgd.tag.json` | The tags applied to it, with the highlighted spans, in Taguette's own export format |
| `tag_summary_export.html` | Every highlight grouped by tag, which is the document you actually analyse from |

Taguette is free, open source, and runs locally (`pip install taguette`,
then `taguette`) or on the hosted service. It does one thing: highlight a
span of text and attach a tag. That is the whole of qualitative coding, and
the expensive tools do not do it better.

## The method, in the order it happens

**1. Decide the coding frame before opening the transcript.** A codebook of
eight to fifteen tags, each with a one-line definition and an example, drawn
from the evaluation questions. Tags invented while reading are fine and
should be added, but a frame that exists only in the coder's head cannot be
applied by a second coder, and a second coder is the whole check.

**2. Code the same two transcripts independently, then compare.** Where two
coders tag the same passage differently, the definition is ambiguous. Fix
the definition, not the coder. Do this before coding the other thirty.

**3. Code for what is said, not for what you expected.** The tag
`barrier_transport` goes on a passage about the bus not coming, whether or
not the evaluation question was about transport. Tags for the questions you
came with are necessary; tags for what the respondents brought are where the
finding is.

**4. Export by tag, and read each tag's passages together.** That is what
`tag_summary_export.html` is. A theme is a tag whose passages, read
together, say something the individual quotes did not.

**5. Count, carefully.** "Eleven of fourteen groups raised transport
unprompted" is a defensible sentence. "78 per cent of respondents cited
transport as a barrier" is the same fact dressed as a survey result, and a
focus group is not a sample.

## What this cannot do

Taguette has no query language, no co-occurrence matrix, no inter-coder
statistic. For a study with a hundred transcripts and three coders, that
matters, and NVivo or MAXQDA earn their price. For an evaluation with
fifteen focus groups and one coder checked by a second, they do not.

## Related

`../visual_ethnography_descript/` for the same discipline applied to recorded
rather than transcribed material. `../annotated_research/annotation_scheme.md`
tag **[MEASURE]** for what a self-reported answer in a group setting is
evidence of.
