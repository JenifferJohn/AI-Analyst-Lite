def validate_query_columns(query, df_columns):
    tokens = query.replace(",", " ").split()

    used_cols = [t for t in tokens if t in df_columns]

    invalid = [t for t in tokens if t.isidentifier() and t not in df_columns]

    if invalid:
        raise ValueError(f"Invalid columns used: {invalid}")

    return True