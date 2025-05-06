# Data Flow Documentation

This file explains the typical flow of data through the InsightStack toolkit.

## 🔄 Typical Workflow:

1. **Raw Data Entry**
   - Source: External surveys, XLSForms, CSV, STATA/SPSS
   - Tools: `survey_to_codebook/`, `data_validation/`

2. **Data Validation**
   - Scripts check for:
     - Missing values
     - Out-of-range entries
     - Duplicates
   - Folder: `data_validation/`

3. **Labeling Variables**
   - Apply human-readable labels to variables
   - Folder: `label_variables/`

4. **Exploration & Analysis**
   - Can now run:
     - Summary statistics
     - Regressions
     - Visualizations
   - Folder: `replication/` or use external tools

5. **Documentation**
   - Generate Markdown codebooks from XLSForms
   - Folder: `survey_to_codebook/`

6. **Archival & Replication**
   - Structure analysis for reuse or publication
   - Folder: `replication/`