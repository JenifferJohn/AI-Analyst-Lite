def generate_insights(df):
    return f"""
Insights:

- Rows: {len(df)}
- Columns: {list(df.columns)}

- Data processed successfully.
"""