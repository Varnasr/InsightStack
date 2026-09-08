import pandas as pd

def xlsform_to_codebook(xls_path, output_path="output_codebook.md"):
    survey = pd.read_excel(xls_path, sheet_name="survey")
    choices = pd.read_excel(xls_path, sheet_name="choices")

    grouped_choices = choices.groupby('list_name')

    with open(output_path, "w") as f:
        f.write("# Codebook\n\n")
        for _, row in survey.iterrows():
            f.write(f"## {row['name']}\n")
            f.write(f"**Label**: {row['label']}\n\n")
            f.write(f"**Type**: {row['type']}\n\n")

            if "select_one" in row['type']:
                list_name = row['type'].split()[1]
                if list_name in grouped_choices.groups:
                    f.write("**Choices:**\n")
                    for _, c_row in grouped_choices.get_group(list_name).iterrows():
                        f.write(f"- {c_row['name']}: {c_row['label']}\n")
                    f.write("\n")
            f.write("---\n\n")

# Example usage:
# xlsform_to_codebook("sample_xlsform.xlsx")