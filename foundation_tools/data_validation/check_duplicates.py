import pandas as pd

def check_duplicates(df, id_column):
    dupes = df[df.duplicated(subset=[id_column], keep=False)]
    print(f"Found {dupes.shape[0]} duplicate rows based on '{id_column}'")
    return dupes