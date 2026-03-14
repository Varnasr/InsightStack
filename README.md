# InsightStack

**MEL tools, calculators, and research documentation for development work.**

[![Part of OpenStacks](https://img.shields.io/badge/Part%20of-OpenStacks-blue)](https://openstacks.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15245182.svg)](https://doi.org/10.5281/zenodo.15245182)

> In development work, we talk about knowledge — but rarely structure it. InsightStack organises the tools, templates, and workflows that make research, evaluation, and program design actually work.

---

## What This Is

InsightStack is a collection of practical scripts, templates, and tools for **monitoring, evaluation, and learning (MEL)** work in the development sector. It covers research documentation, data validation, econometrics, qualitative coding, system dynamics modelling, and visual storytelling.

This is the **knowledge systems layer** of [OpenStacks for Change](https://openstacks.dev) — an open ecosystem of tools for public interest research and evaluation.

## What's Inside

| Directory | What It Contains | Language |
|-----------|-----------------|----------|
| `calculators/` | MEL calculators (sample size, power analysis, cost-effectiveness) | Stata, Python |
| `stata_snippets/` | Reusable Stata code for common analysis tasks | Stata |
| `spss_scripts/` | SPSS syntax for survey analysis | SPSS |
| `econometrics/` | Regression, DiD, RDD, and causal inference templates | Stata, R |
| `data_validation/` | Data cleaning and validation workflows | Python |
| `label_variables/` | Variable labelling and codebook generation | Stata |
| `survey_to_codebook/` | Survey instrument to codebook conversion tools | Python |
| `observable_notebooks/` | Interactive Observable notebooks for data exploration | JavaScript |
| `excalidraw_frameworks/` | Visual frameworks and diagrams for program design | Excalidraw |
| `miro/` | Miro board templates for participatory analysis | Miro |
| `flourish_charts/` | Chart templates for Flourish data visualisation | JSON |
| `powerbi_reports/` | Power BI report templates | PBIX |
| `kumu_maps/` | Network and systems mapping templates | Kumu |
| `vensim/` | System dynamics models | Vensim |
| `taguette_coding/` | Qualitative coding workflows | Taguette |
| `visual_ethnography_descript/` | Ethnographic documentation tools | Descript |
| `latex/` | LaTeX templates for research reports | TeX |
| `writing_guides/` | Style guides and writing templates | Markdown |
| `annotated_research/` | Annotated bibliography and research notes | Markdown |
| `learning_layers/` | Learning design frameworks | Markdown |
| `learning_library/` | Curated learning resources | Markdown |
| `replication/` | Replication files for published analysis | Various |
| `sample_data/` | Practice datasets for testing workflows | CSV |
| `tests/` | Test scripts for validation | Various |
| `workflows/` | End-to-end analysis workflow guides | Markdown |
| `docs/` | Additional documentation | Markdown |

## Getting Started

1. **Browse by need** — Each directory is self-contained. Pick the tool that matches your task.
2. **Check the sample data** — Use `sample_data/` to test scripts before using your own data.
3. **Read the workflows** — `workflows/` contains step-by-step guides that tie multiple tools together.

### Prerequisites

Different tools require different software:
- **Stata 15+** for Stata scripts
- **Python 3.8+** with pandas, statsmodels for Python scripts
- **R 4.0+** with tidyverse for R scripts
- **Observable** account for notebooks (free tier works)
- **Flourish**, **Miro**, **Kumu** accounts for visual tools (free tiers available)

## How It Connects

InsightStack is one of several stacks in the [OpenStacks](https://openstacks.dev) ecosystem:

| Stack | Focus | Link |
|-------|-------|------|
| **InsightStack** (this repo) | MEL tools, calculators, documentation | You are here |
| [FieldStack](https://github.com/Varnasr/FieldStack) | R notebooks for fieldwork & evaluation | Applied data work |
| [EquityStack](https://github.com/Varnasr/EquityStack) | Python workflows for development data | Data pipelines |
| [SignalStack](https://github.com/Varnasr/SignalStack) | Research Rundown newsletter archive | Knowledge curation |

## Contributing

Contributions welcome — especially from practitioners who use these tools in real fieldwork. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Useful contributions include:
- New calculator templates (sample size, power, cost-effectiveness)
- Stata/R/Python scripts for common MEL tasks
- Annotated research examples
- Workflow documentation from your own projects (anonymised)

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

**Created by [Varna Sri Raman](https://github.com/Varnasr)** — Development Economist & Social Researcher
