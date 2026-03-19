from data_engine import get_schema, get_column_info, run_query, validate_sql
from insight_engine import generate_insights
from chart_engine import generate_chart_safe
from llm import ask_llm
from utils import match_columns, validate_user_query, get_cached_result, set_cache, Timer


def extract_entities(query):
    prompt = f"""
    Extract:
    metric, dimensions

    Query: {query}

    Return JSON.
    """
    return eval(ask_llm(prompt))


def run_agent(query, profile, resolved=None):

    timer = Timer()

    try:
        validate_user_query(query)

        cached = get_cached_result(query)
        if cached:
            return cached

        schema = get_schema()
        column_info = get_column_info()
        columns = list(column_info.keys())

        entities = extract_entities(query)

        metric = entities.get("metric", "")
        dimensions = entities.get("dimensions", [])

        # 🔹 If already resolved from UI
        if resolved:
            mapping = resolved
        else:
            mapping = match_columns([metric] + dimensions, columns)

            # Need clarification
            for k, v in mapping.items():
                if len(v) == 0 or len(v) > 1:
                    return {
                        "clarification": True,
                        "mapping": mapping,
                        "message": "Please clarify your intent "
                    }

        # Resolve mapping
        mapping = {k: v[0] if isinstance(v, list) else v for k, v in mapping.items()}

        # Generate SQL
        sql_prompt = f"""
        Schema: {schema}
        Mapping: {mapping}

        Generate SQL only.
        """

        sql = ask_llm(sql_prompt)

        valid, _ = validate_sql(sql)
        if not valid:
            return fallback()

        data = run_query(sql)

        if data.empty:
            return fallback()

        insights = generate_insights(data)

        if "Technical" in profile:
            insights += "\n\n🔍 Deeper analysis completed."

        chart = generate_chart_safe(data)

        result = {
            "insights": insights,
            "chart": chart,
            "time": timer.end()
        }

        set_cache(query, result)
        return result

    except:
        return fallback()


def fallback():
    return {
        "insights": """
 I couldn’t fully process that.

Try:
- Show trend over time
- Top 5 categories
- Summarize insights
""",
        "chart": None,
        "time": 0
    }