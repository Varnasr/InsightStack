# 🧮 Education Needs Projection Calculator – General Logic

This tool helps districts or planners estimate how many schools are needed over a future period based on population growth and existing infrastructure.

---

## 🔢 Inputs Required

1. **Current school-age population** (ages 6–14)
2. **Annual population growth rate** (e.g., 1.85%)
3. **Number of years to project** (e.g., 3 years from now)
4. **Current number of schools** by type:
   - Primary
   - Middle
   - Secondary/Sr. Secondary
5. **Norms**: max students per school (e.g., 150 per primary school)

---

## 📈 Steps Used in Projection

1. **Project population over N years**:

   ```
   Year 1: P1 = P0 × (1 + g)
   Year 2: P2 = P1 × (1 + g)
   ...
   Year N: PN = PN-1 × (1 + g)
   ```

   Where:
   - P0 = current school-age population
   - g = annual growth rate (in decimal)

2. **Estimate schools needed**:

   ```
   Schools Needed = Projected Population / Norm per School
   ```

   Apply separately for each school type if needed.

3. **Calculate school gap**:

   ```
   Gap = Schools Needed - Current Number of Schools
   ```

---

## 🧠 Example

If you have 92,000 children aged 6–14 today, with a 1.85% growth rate, and want to project 3 years out:

```
Year 1: 92,000 × 1.0185 = 93,702
Year 2: 93,702 × 1.0185 = 95,435
Year 3: 95,435 × 1.0185 = 97,201
```

Then, if norm is 150 students per school:

```
Schools Needed = 97,201 / 150 ≈ 648
Current Schools = 584
Gap = 648 - 584 = 64 more schools needed
```

---

Use this calculator for any district. Khunti was used as an illustration.
