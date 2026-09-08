def scan_ranges(df, rules):
    errors = {}
    for var, (min_val, max_val) in rules.items():
        if var in df.columns:
            invalid = df[(df[var] < min_val) | (df[var] > max_val)]
            if not invalid.empty:
                errors[var] = invalid
                print(f"{invalid.shape[0]} rows out of range in '{var}'")
    return errors