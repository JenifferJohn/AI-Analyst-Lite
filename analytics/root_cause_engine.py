def discover_root_cause(df):
    if df is None:
        return {}

    target = "Sales Value (In INR)"
    numeric_cols = df.select_dtypes(include="number").columns

    correlations = {}

    for col in numeric_cols:
        if col != target:
            corr = df[target].corr(df[col])
            correlations[col] = float(corr)

    sorted_corr = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)

    return dict(sorted_corr[:5])