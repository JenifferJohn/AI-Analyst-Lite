def generate_insights(df):
    if df is None or df.empty:
        return "No data available"

    cols = df.columns.tolist()

    if "total_sales" in cols:
        val = float(df["total_sales"].iloc[0])
        return f"Total Sales = {round(val, 2)}"

    if "sales" in cols:
        total = float(df["sales"].sum())
        return f"Aggregated Sales = {round(total, 2)}"

    return "Insight generated from dataset"