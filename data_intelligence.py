def analyze_dataset(df):

    metrics = []
    dimensions = []

    for col in df.columns:

        if df[col].dtype == "object":
            dimensions.append(col)
        else:
            metrics.append(col)

    time_col = None

    for c in df.columns:
        if any(x in c for x in ["date","month","year"]):
            time_col = c

    return {
        "metrics":metrics,
        "dimensions":dimensions,
        "time":time_col
    }