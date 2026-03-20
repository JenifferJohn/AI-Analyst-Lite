import pandas as pd


def detect_column_types(df):
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    date_cols = df.select_dtypes(include=["datetime"]).columns.tolist()

    return numeric_cols, categorical_cols, date_cols


def generate_smart_questions(df):
    questions = []

    numeric_cols, categorical_cols, date_cols = detect_column_types(df)

    # --- Basic Aggregations ---
    for col in numeric_cols:
        questions.append(f"What is total {col}?")
        questions.append(f"What is average {col}?")

    # --- Group By ---
    if numeric_cols and categorical_cols:
        for num in numeric_cols[:2]:  # limit to avoid overload
            for cat in categorical_cols[:2]:
                questions.append(f"{num} by {cat}")
                questions.append(f"Top 5 {cat} by {num}")

    # --- Trends ---
    if numeric_cols and date_cols:
        for num in numeric_cols[:1]:
            for date in date_cols[:1]:
                questions.append(f"{num} over time")
                questions.append(f"Monthly trend of {num}")

    # --- Rankings ---
    if numeric_cols and categorical_cols:
        questions.append(f"Which {categorical_cols[0]} has highest {numeric_cols[0]}?")
        questions.append(f"Lowest {categorical_cols[0]} by {numeric_cols[0]}")

    return list(set(questions))[:10]  # limit to 10