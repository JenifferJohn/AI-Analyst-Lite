import pandas as pd


def analyze_dataset(df):

    metrics = []
    dimensions = []
    time_col = None

    for col in df.columns:

        col_lower = col.lower()
        # detect time column
        if any(x in col_lower for x in ["date", "month", "year", "week"]):
            time_col = col

        # numeric columns = metrics
        if pd.api.types.is_numeric_dtype(df[col]):
            metrics.append(col)

        else:
            dimensions.append(col)

    # fallback: if no metrics detected
    if len(metrics) == 0:

        numeric_cols = df.select_dtypes(include=["int64","float64"]).columns.tolist()

        metrics = numeric_cols

    return {
        "metrics": metrics,
        "dimensions": dimensions,
        "time": time_col
    }