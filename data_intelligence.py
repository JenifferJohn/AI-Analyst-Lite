import pandas as pd


def analyze_dataset(df):

    metrics = []
    dimensions = []
    time_col = None

    for col in df.columns:

        col_l = col.lower()

        if any(x in col_l for x in ["date","month","year","week"]):
            time_col = col

        if pd.api.types.is_numeric_dtype(df[col]):
            metrics.append(col)
        else:
            dimensions.append(col)

    if not metrics:
        metrics = df.select_dtypes(include=["int64","float64"]).columns.tolist()

    return {
        "metrics": metrics,
        "dimensions": dimensions,
        "time": time_col
    }



def detect_date_candidates(df):

    date_keywords = ["date", "month", "year", "week", "day"]

    candidates = []

    for col in df.columns:

        col_l = col.lower()

        # keyword detection
        if any(k in col_l for k in date_keywords):
            candidates.append(col)
            continue

        # datetime type
        if str(df[col].dtype).startswith("datetime"):
            candidates.append(col)

    return candidates