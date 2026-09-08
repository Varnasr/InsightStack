# Power BI Reports (Curated for MEL in India)

This folder does not contain a live `.pbix` file, but instead links to curated, real downloadable Power BI reports and a detailed MEL-specific adaptation note.

## 🔗 Download a Working Power BI File
We recommend starting with this official sample:
➡️ [Human Resources Sample PBIX from Microsoft](https://learn.microsoft.com/en-us/power-bi/create-reports/sample-datasets#human-resources-sample-pbix-file)

It opens in Power BI Desktop and contains layout logic that is easily repurposable.

---

## 🧠 How to Adapt for MEL (Monitoring, Evaluation & Learning)

Power BI is an excellent tool for MEL reporting in India. Here's how to make the most of it:

### 1. **What to Use It For**
- Dashboarding program indicators (coverage, dropout, access, supply chains)
- Summarizing evaluation rounds (baseline–endline comparisons)
- Real-time performance monitoring for government/NGO programs
- Gender or equity disaggregated tracking

---

### 2. **Key Power BI Features to Leverage**
| Feature | MEL Adaptation |
|--------|----------------|
| **Slicers** | Filter indicators by gender, district, age group |
| **Tooltips** | Add insights on survey rounds, confidence intervals |
| **Drillthrough** | Move from summary indicator → village/block view |
| **Bookmarks** | Save different MEL views (e.g., donor vs internal dashboard) |
| **Conditional Formatting** | Color-code whether program targets were met or missed |
| **Dynamic Titles** | Reflect user filters in chart titles automatically |

---

### 3. **Steps to Adapt a PBIX File**
1. Open the sample `.pbix` in Power BI Desktop
2. Replace the dummy dataset with your own (from Excel, CSV, SQL, etc.)
3. Customize visuals:
   - Change indicator names
   - Apply disaggregation by caste, gender, block
   - Use conditional formatting for thresholds
4. Add **navigation tabs** (program overview, district performance, field reports)
5. Export the dashboard as PDF, PNG, or share via Power BI Service

---

### 4. **Tips for Field Teams in India**
- Work in local languages: Power BI allows Unicode fonts
- Use offline Excel exports for teams without internet access
- Align visual colors with government schemes or SDG colors
- Share via WhatsApp as image exports when needed

---

## 📂 Folder Contents
- `mel_dashboard_screenshot.png` – Screenshot of a MEL-style Power BI layout
- `README.md` – This guide

## 🧾 License
This curation and documentation is public domain. The linked `.pbix` belongs to Microsoft under their sample datasets license.