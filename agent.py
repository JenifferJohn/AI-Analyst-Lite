from engines import analytics_engine, chart_engine, root_cause_engine
from llm import ask_llm


def route_query(query):

    q = query.lower()

    # chart queries
    if any(word in q for word in ["chart", "plot", "graph", "distribution"]):
        return "chart"

    # correlation queries
    if any(word in q for word in ["correlation", "correlate", "relationship", "impact"]):
        return "rootcause"

    if any(word in q for word in ["why", "reason", "driver"]):
        return "rootcause"

    # reasoning queries
    if any(word in q for word in ["trend", "insight", "analysis", "pattern"]):
        return "reasoning"

    # aggregation queries
    if any(word in q for word in ["total", "sum", "average", "mean", "max", "min", "count"]):
        return "analytics"

    return "reasoning"


def detect_intent_columns(query, df):

    query_words = query.lower().replace("?", "").split()
    matched = []

    for col in df.columns:
        col_words = col.lower().replace("_", " ").split()
        for q in query_words:
            for cw in col_words:
                if q in cw or cw in q:
                    matched.append(col)

    return list(set(matched))


def run_agent(query, df, persona, selected_column=None):
    matched_columns = detect_intent_columns(query, df)

    if selected_column:
        matched_columns = [selected_column]

    # no column detected
    if len(matched_columns) == 0:
        return {
            "type": "clarification",
            "message": "I could not identify a dataset column related to your question. Please mention a metric like sales, volume, price, etc."
        }

    # multiple matches → ask user
    if len(matched_columns) > 1:
        return {
            "type": "clarification",
            "message": "Multiple relevant columns found. Which one should I use?",
            "options": matched_columns
        }

    # single match
    selected_column = matched_columns[0]
    route = route_query(query)

    if route == "rootcause":
        return root_cause_engine(df, selected_column)

    if route == "chart":
        return chart_engine(df, selected_column)

    if route == "analytics":
        return analytics_engine(df, selected_column)

    # reasoning fallback (LLM)
    schema = df.dtypes.to_string()
    sample = df.head(10).to_string()

    summary = f"""
DATASET SCHEMA:
{schema}

SAMPLE DATA:
{sample}

TARGET COLUMN:
{selected_column}
"""

    return ask_llm(query, summary, persona)