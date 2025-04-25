# XLSForm to Markdown Codebook Converter

This tool converts an XLSForm with `survey` and `choices` sheets into a clean Markdown codebook.

## How to Use

1. Place your XLSForm in this folder.
2. Run the script:
```bash
python xlsform_to_codebook.py
```
3. It will generate `output_codebook.md` with variable names, labels, types, and options.

Works best with forms using `select_one` type choices.