from engines import analytics_engine, chart_engine, root_cause_engine
from llm import ask_llm
from guardrails import dataset_contains_keywords


def route_query(query):

    q = query.lower()

    if "chart" in q or "plot" in q or "graph" in q:
        return "chart"

    if "why" in q or "reason" in q or "root cause" in q:
        return "rootcause"

    if "trend" in q or "insight" in q or "analysis" in q:
        return "reasoning"

    return "analytics"

def map_query_columns(query, df):

    query_words = query.lower().split()

    columns = df.columns.tolist()

    matched_columns = []

    for col in columns:

        col_words = col.lower().replace("_", " ").split()

        for q in query_words:

            for cw in col_words:

                if q in cw or cw in q:
                    matched_columns.append(col)

    return list(set(matched_columns))


def run_agent(query, df, persona):

    matched_columns = map_query_columns(query, df)

    route = route_query(query)

    if route == "analytics":
        return analytics_engine(df, query)

    if route == "chart":
        return chart_engine(df)

    if route == "rootcause":
        return root_cause_engine(df)

    if route == "reasoning":

        schema = df.dtypes.to_string()
        sample = df.head(10).to_string()

        summary = f"""
DATASET COLUMNS:
{df.columns.tolist()}

MATCHED COLUMNS FROM QUERY:
{matched_columns}

DATASET SCHEMA:
{schema}

SAMPLE DATA:
{sample}
"""

        return ask_llm(query, summary, persona)

        return ask_llm(query, summary, persona)