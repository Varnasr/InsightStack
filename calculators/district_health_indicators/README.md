# 🩺 District Health Indicator Estimator

This tool helps estimate district-level health indicators using state NFHS data and contextual adjustments.

---

## 📦 Files

- `health_indicators_calculator.html`: Calculator to adjust state NFHS values using contextual multipliers
- `health_indicators_logic.md`: Markdown explanation of how the projection logic works
- `README.md`: This file

---

## 🧠 How It Works

You enter:
- State-level value (e.g., % of institutional deliveries from NFHS)
- Contextual inputs:
  - Health infrastructure (low/average/high)
  - Road access (poor/average/good)
  - Tribal/SC/ST population density (high/medium/low)

The calculator multiplies the state value by three factors to provide a district-specific estimate.

---

📍 Example: Chitrakoot, Uttar Pradesh
Assume state value is 72.4% for institutional deliveries, with:
- Low infra (0.9)
- Average roads (1.0)
- High tribal/SC/ST density (0.9)

Result:
72.4 × 0.9 × 1.0 × 0.9 ≈ 58.6% (adjusted estimate)
