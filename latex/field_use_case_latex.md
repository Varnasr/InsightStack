
# 📚 Field Use Case: Using LaTeX for Community Documentation in Assam

## Context

In late 2022, a small community foundation in Assam needed to produce a multilingual health report based on their maternal and child health program across five blocks. The report had to include: charts, Devanagari and Assamese script, consistent formatting, and low-bandwidth shareability. Their original draft in MS Word had formatting inconsistencies, lost images, and broken fonts when exported to PDF.

## Solution: Switch to LaTeX

An external researcher supporting the project rebuilt the entire report in LaTeX using Overleaf. The setup included:
- `polyglossia` for Hindi and Assamese text
- `fontspec` with `Lohit Devanagari` and `Tunga`
- Tables, figures, and graphs embedded with auto-captioning
- Clean, paginated PDF export shared via WhatsApp and email

## Why It Worked

- **Reliable Fonts**: All regional script text rendered clearly across devices
- **Reusable Templates**: The format was reused for two subsequent block-level reports
- **Offline Ready**: Once compiled, the PDFs were lightweight and stable
- **Accessible**: Community members with minimal tech skills could read or print the output

## Challenge

Some team members found the `.tex` syntax intimidating at first. This was resolved by preparing a comment-rich starter template and pairing up researchers with Overleaf access.

## Tip for NGOs

If you regularly produce bilingual reports, shift your writing process to LaTeX for clean outputs, long-term archiving, and collaboration — especially when translating across English, Hindi, and regional scripts.
