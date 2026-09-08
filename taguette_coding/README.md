# Qualitative coding with Taguette

One focus group discussion coded start to finish: the transcript, the tag
file, and the export that goes to analysis.

| File | What it is |
| --- | --- |
| `chhattisgarh_chw_fgd.txt` | A focus group discussion with community health workers. Illustrative, not a real group |
| `chhattisgarh_chw_fgd.tag.json` | The tags and highlighted spans, in Taguette's export format |
| `tag_summary_export.html` | Every highlight grouped by tag |

Taguette is free and open source. It runs locally (`pip install taguette`,
then `taguette`) or on the hosted service. It highlights a span of text and
attaches a tag.

## Method

1. Decide the coding frame before opening the transcript: eight to fifteen
   tags, each with a one-line definition and an example, drawn from the
   evaluation questions. Add tags while reading, but write them down.
2. Code the same two transcripts independently, then compare. Where two
   coders differ on a passage, fix the definition.
3. Code what is said, not what you expected. `barrier_transport` goes on a
   passage about the bus not coming whether or not transport was a question.
4. Export by tag and read each tag's passages together. That is
   `tag_summary_export.html`.
5. Count carefully. "Eleven of fourteen groups raised transport unprompted" is
   defensible. "78 per cent of respondents cited transport" is not, because a
   focus group is not a sample.

## Limits

Taguette has no query language, co-occurrence matrix or inter-coder
statistic. For a hundred transcripts and three coders, NVivo or MAXQDA are
worth their price. For fifteen focus groups and one coder checked by a
second, they are not.

Related: `../visual_ethnography_descript/` for recorded material;
`../annotated_research/annotation_scheme.md`, tag **[MEASURE]**.
