def enhance_column_metadata(df):
    metadata = {}

    for col in df.columns:
        desc = col.replace("_", " ").title()

        if "sales" in col:
            desc += " (Revenue related metric)"
        elif "date" in col:
            desc += " (Time dimension)"
        elif "id" in col:
            desc += " (Identifier)"

        metadata[col] = desc

    return metadata