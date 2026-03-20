import pandas as pd


def fast_execute(query, df):
    q = query.lower()

    # -------------------------
    # SALES PERFORMANCE
    # -------------------------
    if "total sales" in q or "total sales value" in q:
        col = [c for c in df.columns if "sales value" in c.lower()]
        if col:
            return {"answer": df[col[0]].sum()}

    if "sales by market" in q:
        col = [c for c in df.columns if "sales value" in c.lower()][0]
        grp = [c for c in df.columns if "market" in c.lower()][0]
        result = df.groupby(grp)[col].sum().reset_index()
        return {"data": result.to_dict(orient="records")}

    if "sales by product" in q:
        col = [c for c in df.columns if "sales value" in c.lower()][0]
        grp = [c for c in df.columns if "product" in c.lower()][0]
        result = df.groupby(grp)[col].sum().reset_index()
        return {"data": result.to_dict(orient="records")}

    # -------------------------
    # GROWTH ANALYSIS
    # -------------------------
    if "growth" in q or "trend" in q:
        val_col = [c for c in df.columns if "sales value" in c.lower()][0]
        time_col = [c for c in df.columns if "month" in c.lower()][0]

        temp = df.copy()
        temp = temp.sort_values(time_col)

        temp["growth"] = temp[val_col].pct_change()
        return {"data": temp[[time_col, "growth"]].dropna().to_dict(orient="records")}

    return None