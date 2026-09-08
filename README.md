# InsightStack

**MEL tools, calculators, and research documentation for development work.**

[![Part of OpenStacks](https://img.shields.io/badge/Part%20of-OpenStacks-blue)](https://openstacks.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15245182.svg)](https://doi.org/10.5281/zenodo.15245182)
[![Status: Stable](https://img.shields.io/badge/Status-Stable-0969da?style=flat-square)](https://github.com/Varnasr/OpenStacks-for-Change/blob/main/MAINTENANCE.md)

> In development work, we talk about knowledge — but rarely structure it. InsightStack organises the tools, templates, and workflows that make research, evaluation, and program design actually work.

> **Status: Stable.** This repository works and is correct, but it is not under active
> development. Bug reports are welcome and issues stay open; new features are unlikely,
> and replies are measured in weeks rather than days. Dependencies are pinned deliberately
> so that a clone still runs years from now. See the [maintenance policy](https://github.com/Varnasr/OpenStacks-for-Change/blob/main/MAINTENANCE.md).

---

## What This Is

InsightStack is a collection of practical scripts, templates, and tools for **monitoring, evaluation, and learning (MEL)** work in the development sector. It covers data validation, survey analysis, system dynamics modelling, network analysis, qualitative coding, and visual storytelling.

This is the **knowledge systems layer** of [OpenStacks for Change](https://openstacks.dev) — an open ecosystem of tools for public interest research and evaluation.

## What's Inside

### Analysis Tools

| Directory | What It Does | Language | Status |
|-----------|-------------|----------|--------|
| `data_starters/` | Loaders for real public-use survey microdata, one folder per dataset. DHS across South Asia, and PLFS | Stata, R, Python | Ready |
| `calculators/` | District-level calculators for health, education, finance, environment, and population | HTML, JavaScript | Ready |
| `data_validation/` | Rule-driven validation from a data dictionary: duplicates, required, ranges, allowed values, types, name style, column set, cross-file ids; one issue row per problem, by identifier | Python (18 tests); Stata, R, SPSS companions |
| `stata_snippets/` | Reusable Stata code: data management, graphs, regression, impact evaluation, surveys | Stata | Ready |
| `spss_scripts/` | Survey analysis syntax: cleaning, regression, missing data, frequencies | SPSS | Ready |
| `network_effects_sni/` | Peer effects estimation, centrality analysis, diffusion modelling for SHG networks | Python | Ready |
| `replication/` | A replication package that verifies itself: one entry point, a recorded result, a Python-against-R cross-check, and a test that the verification can fail | Python, R (4 tests) |
| `label_variables/` | Variable and value labels from a dictionary, written into `.dta` and `.sav` where they survive; round-trips both ways | Python (8 tests); Stata, R, SPSS companions |
| `survey_to_codebook/` | XLSForm to Markdown codebook and to a label dictionary; resolves groups, repeats and choice lists; reports form defects | Python (9 tests) |
| `econometrics/` | Causal inference: DiD, PSM, IV/2SLS, RDD, sensitivity analysis — with Python, R, and sample data | Python, R | Ready |

### Visual and Interactive Tools

| Directory | What It Does | Tool |
|-----------|-------------|------|
| `vensim/` | 8 system dynamics models (health, agriculture, climate, migration, education) | Vensim |
| `tool_notes/` | Nine tool notes (Excalidraw, Kumu, Observable, RawGraphs, Flourish, Power BI, Miro, Excel, LaTeX): when each is worth the setup, when it is not, what goes wrong, with one worked file each | Notes |

### Knowledge and Documentation

| Directory | What It Contains |
|-----------|-----------------|
| `learning_library/` | Curated PDFs across 10 categories: programming, data science, research methods, AI tools, MLE resources |
| `writing_guides/` | Theory of change, results chain, evaluation report structure, policy brief, writing about uncertainty; the verb is decided by the design | Markdown |
| `eval_docs/` | Logframe template, indicator reference sheet, MEL framework outline, indicator guidance, with a completed example | Markdown, CSV, XLSX |
| `KM_tools/` | Folder structure, project README template, file naming, tagging | Markdown |
| `annotated_research/` | Five research briefs marked up with one eight-tag annotation scheme, weakest design to strongest; illustrative, for teaching critical reading | Markdown |
| `learning_layers/` | Embedding learning in the MEL cycle as scheduled decisions at three tempos | Markdown, PDF |
| `taguette_coding/` | One focus group coded start to finish in Taguette, with the method: frame first, double-code two transcripts, count carefully | Qualitative |
| `visual_ethnography_descript/` | From recording to clip to quote: three consents, quotes checked against audio, clips cut with context visible | Qualitative |
| `workflows/` | End-to-end analysis workflow guides |

## Getting Started

1. **Browse by need** — Each directory is self-contained. Pick the tool that matches your task.
2. **Check the sample data** — Use `sample_data/` and the test data in `data_validation/` to try scripts.
3. **Read the workflows** — `workflows/` ties multiple tools together into end-to-end processes.

### Prerequisites

Different tools require different software:
- **Stata 15+** for Stata scripts and snippets
- **Python 3.8+** with pandas, statsmodels, networkx for Python scripts
- **R 4.0+** with tidyverse for R scripts
- **SPSS** for survey analysis syntax
- **Observable**, **Flourish**, **Miro**, **Kumu** accounts for visual tools (free tiers available)

## How It Connects

InsightStack is one of several stacks in the [OpenStacks](https://openstacks.dev) ecosystem:

| Stack | Focus |
|-------|-------|
| **InsightStack** (this repo) | MEL tools, calculators, research documentation, and loaders for real survey microdata. Stata, Python, R, SPSS |
| [FieldStack](https://github.com/Varnasr/FieldStack) | Field operations while a survey is being collected, and survey analysis after. R |
| [EquityStack](https://github.com/Varnasr/EquityStack) | Equity from a development economics perspective: distributional analysis, the concentration index, and design-based survey estimation. Python |

[openstacks.dev](https://openstacks.dev) is the index for all of it. [SignalStack](https://github.com/Varnasr/SignalStack) is the companion archive for the [Research Rundown](https://researchrundown.substack.com) newsletter, alongside the stacks rather than one of them. [PolicyStack](https://github.com/Varnasr/PolicyStack) is superseded by [PolicyDhara](https://github.com/Varnasr/PolicyDhara). RootStack, BridgeStack and ViewStack are archived.

## Contributing

Contributions welcome — especially from practitioners who use these tools in real fieldwork. See [contributing guidelines](https://github.com/Varnasr/.github/blob/main/CONTRIBUTING.md) for guidelines.

High-impact areas:
- **Econometrics** — causal inference implementations (DiD, PSM, IV, RDD) in Python, R, or Stata
- **Calculators** — new district-level planning tools
- **Stata/SPSS scripts** — analysis templates for common MEL tasks
- **Sample data** — synthetic datasets for testing

## Citation

```bibtex
@software{insightstack,
  author = {Sri Raman, Varna},
  title = {InsightStack: MEL Tools for Development Work},
  url = {https://github.com/Varnasr/InsightStack},
  doi = {10.5281/zenodo.15245182}
}
```

## License

MIT — free to use, modify, and share. See [LICENSE](LICENSE).

---

Part of [OpenStacks for Change](https://openstacks.dev). Created by [Varna Sri Raman](https://on-web.link/varna).
