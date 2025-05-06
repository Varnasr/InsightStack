import pandas as pd

# Load your dataset and dictionary
df = pd.read_csv('your_data_file.csv')
dict_df = pd.read_csv('../input/data_dictionary.csv')

# Create label mapping
labels = dict(zip(dict_df['variable'], dict_df['label']))

# Apply as metadata (example: store in df.attrs or export to separate JSON)
df.attrs['variable_labels'] = labels

# Save as CSV again or export labels separately
df.to_csv('your_data_file_labelled.csv', index=False)