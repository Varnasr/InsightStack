# 🩺 District Health Indicator Projection – General Logic

This tool helps estimate district-level health indicators (e.g., immunization, maternal health) when only state-level NFHS data is available. It uses adjustment factors based on known district context.

---

## 🔢 Inputs

1. **State-level NFHS value** (e.g., institutional deliveries = 72.4%)
2. **Contextual Adjustments**:
   - Health infrastructure (low / average / high)
   - Road access (poor / average / good)
   - Demographics (e.g. high tribal/SC/ST %)

---

## 📈 How the Adjustment Works

We multiply the state value by an adjustment factor based on local context. For example:

```
District Estimate = State Value × Adjustment Factor
```

Each context input adjusts the factor slightly up or down:

| Factor                | Low     | Avg     | High    |
|-----------------------|---------|---------|---------|
| Health Infra          | 0.9     | 1.0     | 1.1     |
| Road Access           | 0.95    | 1.0     | 1.05    |
| Tribal/SC/ST Density  | 0.9     | 1.0     | 1.1     |

The final adjustment is the product of all applicable factors.

---

## 🧠 Example

NFHS State Value (Institutional Deliveries): 72.4%  
Khunti has low infra (0.9), avg roads (1.0), and high tribal % (0.9):

```
Adjusted = 72.4 × 0.9 × 1.0 × 0.9 = ~58.6%
```

This gives a realistic district estimate where full surveys are missing.

---

Use this logic for any district with suitable state reference data.
