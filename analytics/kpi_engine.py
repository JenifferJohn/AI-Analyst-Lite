import pandas as pd


def compute_kpis(df):
    """
    Compute KPI metrics using full dataset (no sampling)
    """
    if df is None or df.empty:
        return {}

    required_cols = ["Month", "Sales Value (In INR)", "Markets"]

    for col in required_cols:
        if col not in df.columns:
            return {}

    df_sorted = df.sort_values("Month")

    latest_month = df_sorted["Month"].max()
    unique_months = df_sorted["Month"].unique()

    if len(unique_months) < 2:
        return {}

    prev_month = unique_months[-2]

    current_sales = df_sorted[df_sorted["Month"] == latest_month]["Sales Value (In INR)"].sum()
    previous_sales = df_sorted[df_sorted["Month"] == prev_month]["Sales Value (In INR)"].sum()

    change = current_sales - previous_sales
    pct_change = (change / previous_sales) * 100 if previous_sales != 0 else 0

    # Top market
    grouped = df.groupby("Markets")["Sales Value (In INR)"].sum()
    top_market = grouped.idxmax()
    top_market_value = grouped.max()

    return {
        "current_sales": float(current_sales),
        "previous_sales": float(previous_sales),
        "change": float(change),
        "pct_change": float(pct_change),
        "top_market": str(top_market),
        "top_market_value": float(top_market_value)
    }