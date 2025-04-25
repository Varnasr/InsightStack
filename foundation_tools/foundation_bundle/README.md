# Foundation Tools for Data Management & Reproducible Research

This master bundle includes five fully built, reusable modules designed to support field research, MEL systems, and reproducible workflows across public interest data work in India.

---

## 📁 Included Modules

### 1. `data_validation/`
Reusable scripts for validating raw or cleaned datasets:
- Duplicate ID checks (Python, Stata, SPSS)
- Variable name validation
- Value range scans
- Code label checks

### 2. `survey_to_codebook/`
Converts an XLSForm to a clean Markdown codebook:
- Input: XLSForm with `survey` and `choices` sheets
- Output: Human-readable `.md` codebook
- Language: Python

### 3. `data_flow.md`
A Markdown template to document how your dataset moved from:
- Raw form → cleaned version → analysis-ready file
- Includes transformation logs, tool tracking, and derived variable mapping

### 4. `label_variables/`
Templates to assign meaningful labels to variables in:
- Python (DataFrame metadata)
- SPSS syntax
- Stata `.do` format

### 5. `replication/`
Basic structure to replicate your core analysis:
- Python regression example
- `requirements.txt`
- `README.md` for clear execution instructions

---

## 🔧 How to Use

Each folder is independent and reusable. Drop into your project directory, adapt paths, and run based on your toolchain (SPSS/Stata/Python).

---

## 🔍 Why This Matters

These tools promote better:
- Research reproducibility
- Field-level data cleaning workflows
- Open knowledge practices
- Institutional memory in long-term programs

This bundle aligns with open standards like DIME (World Bank) and MEL frameworks used by IHCRF, Udaiti, and public health researchers.

---