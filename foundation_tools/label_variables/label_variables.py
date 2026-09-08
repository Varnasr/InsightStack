import pandas as pd

def apply_labels(df, label_dict):
    df.attrs['variable_labels'] = label_dict
    print("Labels applied (stored in DataFrame metadata).")
    return df

# Example usage:
# labels = {'age': 'Age of respondent', 'wages': 'Monthly wages'}
# df = apply_labels(df, labels)