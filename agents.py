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


def run_agent(query, df, persona):

    if not dataset_contains_keywords(query, df):
        return "IRRELEVANT_TO_DATASET"

    route = route_query(query)

    if route == "analytics":
        return analytics_engine(df, query)

    if route == "chart":
        return chart_engine(df)

    if route == "rootcause":
        return root_cause_engine(df)

    if route == "reasoning":

        summary = df.describe().to_string()

        return ask_llm(query, summary, persona)