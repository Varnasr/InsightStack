# InsightStack

MEL tools, calculators, research documentation and loaders for survey
microdata, in Stata, Python, R and SPSS. Part of
[OpenStacks](https://openstacks.dev). Status: Stable, per the family
[maintenance policy](https://github.com/Varnasr/OpenStacks-for-Change/blob/main/MAINTENANCE.md).
DOI: [10.5281/zenodo.15245182](https://doi.org/10.5281/zenodo.15245182).

Site: [varnasr.github.io/InsightStack](https://varnasr.github.io/InsightStack/).

## Code and data

| Directory | What it does | Language |
| --- | --- | --- |
| `data_starters/` | Loaders for DHS (28 surveys, seven South Asian countries) and PLFS (India) that open the files as distributed, with the weight and scale rules applied. Tested on synthetic fixtures; no data ships | Stata, R, Python |
| `calculators/` | Six browser calculators for district planning: population projection, school needs, banking access, district health indicators, block-level estimates, environmental fragility | HTML, JavaScript |
| `econometrics/` | Difference-in-differences, propensity score matching, instrumental variables, regression discontinuity, sensitivity analysis, with sample data | Python, R |
| `stata_snippets/` | 44 do-files: data management, descriptives, regression, impact evaluation, graphs, survey settings | Stata |
| `spss_scripts/` | 20 files: cleaning, recoding, tabulation, regression, Excel export | SPSS |
| `network_effects_sni/` | Centrality, peer association with leave-one-out means, and threshold diffusion for self-help group data. 17 tests | Python |
| `data_validation/` | Checks from a data dictionary: duplicates, required fields, ranges, allowed values, types, column set, cross-file ids. One row per problem. 18 tests | Python; Stata, R, SPSS companions |
| `label_variables/` | Variable and value labels from a dictionary, written into `.dta` and `.sav`. 8 tests | Python; Stata, R, SPSS companions |
| `survey_to_codebook/` | An XLSForm to a Markdown codebook and a label dictionary. 9 tests | Python |
| `replication/` | A replication package with one entry point, a recorded result and an R cross-check. 4 tests | Python, R |
| `vensim/` | Eight system dynamics models | Vensim |

## Documents and notes

| Directory | What it holds |
| --- | --- |
| `tool_notes/` | Nine notes on visual and document tools (Excalidraw, Kumu, Observable, RawGraphs, Flourish, Power BI, Miro, Excel, LaTeX), each with one example file |
| `writing_guides/` | Theory of change, results chain, evaluation report structure, policy brief, writing about uncertainty |
| `eval_docs/` | Logframe, indicator reference sheet and MEL framework templates, with a completed example |
| `annotated_research/` | Five illustrative research briefs annotated with one eight-tag scheme |
| `learning_layers/` | Learning in the MEL cycle as scheduled decisions |
| `KM_tools/` | Folder structure, README template, file naming, tagging |
| `taguette_coding/` | One focus group coded in Taguette, with the method |
| `visual_ethnography_descript/` | Recorded interviews: consent, transcription, clips, quotes |
| `learning_library/` | PDFs and guides in five categories |

## Tests

```
cd data_starters/dhs-south-asia && python make_fixture.py --outdir fixtures
python test_load_dhs.py && Rscript test_load_dhs.R
cd ../plfs-india && python make_fixture.py --outdir fixtures
python test_load_plfs.py && Rscript test_load_plfs.R
python -m network_effects_sni.test_network_effects
python data_validation/test_data_validation.py
python label_variables/test_label_variables.py
python survey_to_codebook/test_survey_to_codebook.py
python replication/test_replication.py
```

All of these run in CI on every pull request. The Stata files are not
tested, since Stata has no free runtime; each carries a fixture check at the
bottom.

## Requirements

Stata 15 or later for the do-files. Python 3.8 or later with pandas,
statsmodels and networkx. R 4.0 or later with tidyverse, survey and haven.
SPSS for the syntax files.

## The family

| Repository | What it is for | Language |
| --- | --- | --- |
| **InsightStack** (this repository) | MEL tools, calculators, research documentation, loaders for survey microdata | Stata, Python, R, SPSS |
| [FieldStack](https://github.com/Varnasr/FieldStack) | Field operations while a survey is in the field; sampling and weighted estimation after | R |
| [EquityStack](https://github.com/Varnasr/EquityStack) | Inequality measurement and design-based survey estimation | Python |

[openstacks.dev](https://openstacks.dev) is the index.
[SignalStack](https://github.com/Varnasr/SignalStack) is the companion archive
for the [Research Rundown](https://varna.substack.com) newsletter, beside the
stacks rather than one of them.
[PolicyStack](https://github.com/Varnasr/PolicyStack) is superseded by
[PolicyDhara](https://github.com/Varnasr/PolicyDhara). RootStack, BridgeStack
and ViewStack are archived.

## Citation and license

```bibtex
@software{insightstack,
  author = {Sri Raman, Varna},
  title = {InsightStack: MEL tools, calculators and survey data loaders},
  url = {https://github.com/Varnasr/InsightStack},
  doi = {10.5281/zenodo.15245182}
}
```

MIT. See [LICENSE](LICENSE).
