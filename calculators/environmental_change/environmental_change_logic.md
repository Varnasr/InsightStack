# 🌱 Environmental Change Risk Estimation – Logic

This tool estimates climate fragility and environmental risk levels for a district using key ecological indicators.

---

## 🔢 Inputs

- Forest Cover (% of total area)
- Households with Drinking Water Nearby (%)
- Mean Annual Rainfall Deviation (from baseline)
- Mean Temperature Change (°C over baseline)

---

## 📈 Scoring Logic

Each variable is scored between 0–1 and weighted to compute a composite risk score.

| Indicator                 | Weight | Risk Thresholds |
|--------------------------|--------|------------------|
| Forest Cover (%)         | 0.3    | <25% = high risk |
| Drinking Water (%)       | 0.3    | <60% = high risk |
| Rainfall Deviation (mm)  | 0.2    | >100mm = high    |
| Temperature Change (°C)  | 0.2    | >1.5°C = high    |

Risk categories:

- 0.7–1.0 = High Environmental Fragility
- 0.4–0.69 = Moderate Fragility
- <0.4 = Low Risk

---

## 🧠 Example

Forest cover = 21%, Water access = 55%, Rainfall dev = 120mm, Temp rise = 1.8°C

→ Score = Weighted composite = 0.78 → High Fragility Risk

This helps local planners prioritize resilience and climate-linked planning.
