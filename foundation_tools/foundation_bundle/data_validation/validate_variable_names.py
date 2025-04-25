import re

def validate_names(df):
    invalid = [col for col in df.columns if not re.match(r'^[a-z_][a-z0-9_]*$', col)]
    print(f"Invalid variable names: {invalid}")
    return invalid