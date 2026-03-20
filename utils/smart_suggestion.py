import pandas as pd
from utils.smart_naming import generate_column_map


def detect_column_types(df):
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    date_cols = df.select_dtypes(include=["datetime", "datetime64[ns]"]).columns.tolist()
    return numeric_cols, categorical_cols, date_cols


def generate_smart_questions(df):
    if df is None or df.empty:
        return []

    questions = []

    numeric_cols, categorical_cols, date_cols = detect_column_types(df)
    col_map = generate_column_map(df)

    def cname(col):
        return col_map.get(col, col)

    # Aggregations
    for col in numeric_cols[:3]:
        questions.append(f"What is total {cname(col)}?")
        questions.append(f"What is average {cname(col)}?")

    # Group by
    if numeric_cols and categorical_cols:
        for num in numeric_cols[:2]:
            for cat in categorical_cols[:2]:
                questions.append(f"{cname(num)} by {cname(cat)}")
                questions.append(f"Top 5 {cname(cat)} by {cname(num)}")

    # Trends / Growth
    if numeric_cols and date_cols:
        for num in numeric_cols[:1]:
            questions.append(f"{cname(num)} over time")
            questions.append(f"Monthly trend of {cname(num)}")
            questions.append(f"{cname(num)} growth over time")

    # Rankings
    if numeric_cols and categorical_cols:
        questions.append(f"Which {cname(categorical_cols[0])} has highest {cname(numeric_cols[0])}?")
        questions.append(f"Lowest {cname(categorical_cols[0])} by {cname(numeric_cols[0])}")

    # Business-style questions
    if numeric_cols and categorical_cols:
        questions.append(f"Which {cname(categorical_cols[0])} drives most {cname(numeric_cols[0])}?")
        questions.append(f"Contribution of {cname(categorical_cols[0])} to {cname(numeric_cols[0])}")

    # Deduplicate and limit
    questions = list(set(questions))

    return questions[:10]