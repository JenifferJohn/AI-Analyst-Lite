import re


ABBREVIATIONS = {
    "qty": "Quantity",
    "amt": "Amount",
    "rev": "Revenue",
    "num": "Number",
    "cnt": "Count",
    "avg": "Average",
    "pct": "Percentage",
    "id": "ID",
    "vol": "Volume",
    "val": "Value"
}


def clean_column_name(col):
    col = str(col).lower()
    col = col.replace("_", " ").replace("-", " ")
    words = col.split()

    cleaned_words = []
    for w in words:
        if w in ABBREVIATIONS:
            cleaned_words.append(ABBREVIATIONS[w])
        else:
            cleaned_words.append(w.capitalize())

    return " ".join(cleaned_words)


def generate_column_map(df):
    mapping = {}
    for col in df.columns:
        mapping[col] = clean_column_name(col)
    return mapping


def apply_friendly_names(df):
    mapping = generate_column_map(df)
    clean_df = df.rename(columns=mapping)
    return clean_df, mapping


def humanize_query(query, column_map):
    if not column_map:
        return query

    updated_query = query

    for raw, clean in column_map.items():
        pattern = rf"\b{re.escape(raw)}\b"
        updated_query = re.sub(pattern, clean, updated_query, flags=re.IGNORECASE)

    return updated_query