import re

COLUMN_MAP = {}
REVERSE_MAP = {}


def generate_column_map(columns):
    global COLUMN_MAP, REVERSE_MAP

    clean_map = {}

    for col in columns:
        new_col = col.lower()
        new_col = re.sub(r'[%()]', '', new_col)
        new_col = re.sub(r'[^a-z0-9]+', '_', new_col)
        new_col = new_col.strip('_')

        # semantic fixes
        new_col = new_col.replace("chnge", "change")

        clean_map[col] = new_col

    COLUMN_MAP = clean_map
    REVERSE_MAP = {v: k for k, v in clean_map.items()}

    return clean_map


def normalize_dataframe(df):
    col_map = generate_column_map(df.columns)
    df = df.rename(columns=col_map)
    return df


def get_canonical_columns():
    return list(REVERSE_MAP.keys())