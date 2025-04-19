# 🏦 Financial Inclusion Projection Logic

This tool helps estimate how many banking access points (banks, ATMs, CSPs) are needed in a district based on population and service norms.

---

## 🔢 Inputs

- Current district population
- Norm: people per access point (e.g., 2,000 people per bank point)
- Current access points:
  - Commercial Banks
  - Rural Banks
  - ATMs
  - Bank Mitras / CSPs

---

## 📈 Formula

```
Needed Access Points = Population / Norm
Current Total Points = Commercial + Rural + ATMs + Mitras
Gap = Needed - Current
```

---

## 🧠 Example

For a district with:
- Population: 675,000
- Norm: 2,000 people per access point
- Current points: 280

Calculation:
```
Needed = 675,000 / 2,000 = 338
Gap = 338 - 280 = 58 new points needed
```

---

This helps districts plan banking expansion and monitor access equity.
