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
| `calculators/` | District-level calculators for health, education, finance, environment, and population | HTML, JavaScript | Ready |
| `data_validation/` | Data cleaning and validation workflows with intentionally messy test data | Python, R, Stata | Ready |
| `stata_snippets/` | Reusable Stata code: data management, graphs, regression, impact evaluation, surveys | Stata | Ready |
| `spss_scripts/` | Survey analysis syntax: cleaning, regression, missing data, frequencies | SPSS | Ready |
| `network_effects_sni/` | Peer effects estimation, centrality analysis, diffusion modelling for SHG networks | Python | Ready |
| `replication/` | Replication template with parallel Python and R implementations | Python, R | Ready |
| `label_variables/` | Variable labelling and codebook generation | Stata | Ready |
| `survey_to_codebook/` | Survey instrument to codebook conversion | Python | Ready |
| `econometrics/` | Causal inference: DiD, PSM, IV/2SLS, RDD, sensitivity analysis — with Python, R, and sample data | Python, R | Ready |

### Visual and Interactive Tools

| Directory | What It Does | Tool |
|-----------|-------------|------|
| `vensim/` | 8 system dynamics models (health, agriculture, climate, migration, education) | Vensim |
| `observable_notebooks/` | Interactive district vulnerability dashboard | Observable |
| `excalidraw_frameworks/` | MEL framework and ecosystem map diagrams | Excalidraw |
| `flourish_charts/` | Data visualisation templates | Flourish |
| `miro/` | Participatory analysis board templates | Miro |
| `kumu_maps/` | Network and systems mapping | Kumu |
| `powerbi_reports/` | Report templates | Power BI |
| `excel_visuals/` | Excel visualisation templates | Excel |

### Knowledge and Documentation

| Directory | What It Contains |
|-----------|-----------------|
| `learning_library/` | Curated PDFs across 10 categories: programming, data science, research methods, AI tools, MLE resources |
| `writing_guides/` | Style guides and writing templates |
| `annotated_research/` | Annotated bibliography and research notes |
| `learning_layers/` | Learning design frameworks |
| `taguette_coding/` | Qualitative coding workflows |
| `visual_ethnography_descript/` | Ethnographic documentation tools |
| `latex/` | LaTeX templates for research reports |
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
| **InsightStack** (this repo) | MEL tools, calculators, documentation |
| [FieldStack](https://github.com/Varnasr/FieldStack) | R notebooks for fieldwork and evaluation |
| [EquityStack](https://github.com/Varnasr/EquityStack) | Python workflows for development data |
| [SignalStack](https://github.com/Varnasr/SignalStack) | Research Rundown newsletter archive |

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
