
import pandas as pd

# Load data
df = pd.read_csv('../sample_data/sample_data.csv')

# Check missing values
print("Missing values:")
print(df.isnull().sum())

# Check duplicates by ID
print("\nDuplicate rows (by ID):")
print(df[df.duplicated('id')])

# Check invalid gender values
print("\nInvalid gender values (allowed: M, F):")
print(df[~df['gender'].isin(['M', 'F'])])
