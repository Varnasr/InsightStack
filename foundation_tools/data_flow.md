# Data Flow Documentation

This file documents the transformation of a dataset from raw collection to final analysis-ready form.

---

## 📌 Dataset Overview

| Field            | Description                                     |
|------------------|-------------------------------------------------|
| Dataset Name     | we_employment_survey.csv                        |
| Source           | XLSForm via Kobo Toolbox                        |
| Format           | CSV                                             |
| Location         | Jharkhand, India                                |
| Collection Date  | Jan 2025                                        |
| Uploaded By      | field_team_1                                    |

---

## 🧹 Data Cleaning & Transformation Log

| Step No. | Date       | Action                                   | Tool Used   | Notes                                  |
|----------|------------|-------------------------------------------|-------------|----------------------------------------|
| 1        | 2025-01-15 | Removed duplicates on `respondent_id`     | Python      | Used `check_duplicates.py`             |
| 2        | 2025-01-16 | Recoded `education_level` to numeric      | SPSS        | Added ordinal labels                   |
| 3        | 2025-01-17 | Merged with wage_2021.csv                 | Stata       | Merge on `respondent_id`               |
| 4        | 2025-01-18 | Converted wide to long format             | SPSS        | Used `VARSTOCASES`                     |
| 5        | 2025-01-19 | Created `formal_sector` from employment   | Python      | New binary derived variable            |

---

## 🧮 Derived Variables

| Variable Name    | Description                                  | Formula/Source                      |
|------------------|----------------------------------------------|-------------------------------------|
| formal_sector    | Whether respondent is in formal employment   | employment_type recode              |
| age_group        | Age bins: 18–25, 26–35, 36+                  | Binned from `age`                   |
| edu_level_num    | Ordinal numeric version of education_level   | Recoded via SPSS                    |

---

## 📁 Final Output

| File Name                   | Description                           |
|-----------------------------|----------------------------------------|
| we_employment_survey_clean.csv | Cleaned dataset with derived vars     |
| we_employment_survey_long.csv  | Long-form reshaped dataset            |

---

## 🧾 Notes

- This dataset is now ready for regression and stratified analysis.
- Use `data_validation/` and `spss_tools/` references for applied scripts.