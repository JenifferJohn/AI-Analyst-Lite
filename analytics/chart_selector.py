def choose_chart(df):
    if len(df.columns) == 2:
        return "bar"
    elif len(df.columns) > 2:
        return "line"
    return "table"