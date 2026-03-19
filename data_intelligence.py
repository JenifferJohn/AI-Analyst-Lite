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

def detect_target_candidates(df):

    import pandas as pd

    priority_keywords = [
        "sales", "revenue", "value",
        "volume", "price", "amount"
    ]

    scores = []

    for col in df.columns:

        col_l = col.lower()

        score = 0

        # keyword-based scoring
        for kw in priority_keywords:
            if kw in col_l:
                score += 2

        # numeric columns boost
        if pd.api.types.is_numeric_dtype(df[col]):
            score += 1

        scores.append((col, score))

    # sort by score
    ranked = sorted(scores, key=lambda x: x[1], reverse=True)

    # return only meaningful candidates
    return [c[0] for c in ranked if c[1] > 0]