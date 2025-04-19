# 🧱 Block-Level Development Estimation – Logic

This tool helps estimate block-level indicator values by disaggregating district-level data using population or area shares.

---

## 🔢 Inputs

- Total District Population
- Block Population
- District-level indicator value (e.g., number of PHCs, % coverage)

---

## 📈 Disaggregation Logic

### Method 1: Population-Based Disaggregation

```
Block Share = Block Population / District Population
Block Estimate = District Value × Block Share
```

This assumes uniform distribution and is best for counts (e.g., number of schools, facilities).

### Method 2: Area-Based Disaggregation (Optional)

```
Block Share = Block Area / District Area
Block Estimate = District Value × Block Area Share
```

---

## 🧠 Example

District has 600,000 population and 30 PHCs. A block with 75,000 population:

```
Block Share = 75,000 / 600,000 = 0.125
Block PHCs = 30 × 0.125 = 3.75 → ~4 PHCs
```

This provides useful planning estimates where direct block data is missing.
