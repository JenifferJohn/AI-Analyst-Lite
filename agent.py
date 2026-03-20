import json
from data_engine import get_schema, get_column_info, run_query, validate_sql
from insight_engine import generate_insights
from chart_engine import generate_chart_safe
from llm import ask_llm
from utils import StepTimer, validate_user_query, safe_response


def safe_json(x):
    try:
        return json.loads(x)
    except:
        return {}


def llm_mapping(query, columns):
    prompt = f"""
Map query to columns.

Query: {query}
Columns: {columns}

Return JSON:
{{"metric":"","dimensions":[]}}
"""
    return safe_json(ask_llm(prompt))


def generate_sql(query, schema, mapping, error=""):
    prompt = f"""
Schema:
{schema}

Mapping:
{mapping}

Error:
{error}

Generate SELECT SQL only.
"""
    return ask_llm(prompt)


def run_agent(query, profile, stream_callback=None, resolved=None):

    timer = StepTimer()

    try:
        validate_user_query(query)

        schema = get_schema()
        col_info = get_column_info()
        columns = list(col_info.keys())

        # STEP 1
        step = timer.log("🔄 Understanding query")
        if stream_callback:
            stream_callback(f"{step[0]} ({step[1]}s)")

        mapping = resolved if resolved else llm_mapping(query, columns)

        if not mapping.get("metric"):
            return safe_response(
                "I need help selecting the right field 👇",
                {"metric": columns}
            )

        # STEP 2
        step = timer.log("⚡ Generating SQL")
        if stream_callback:
            stream_callback(f"{step[0]} ({step[1]}s)")

        sql = None
        error = ""

        for _ in range(3):
            sql = generate_sql(query, schema, mapping, error)
            valid, msg = validate_sql(sql)
            if valid:
                break
            error = msg

        if not sql:
            return safe_response("Let’s refine your request 👇")

        # STEP 3
        step = timer.log("📊 Fetching data")
        if stream_callback:
            stream_callback(f"{step[0]} ({step[1]}s)")

        data = run_query(sql)

        if data.empty:
            return safe_response(
                "No data found. Try broader query 👇",
                {"Try": ["Show overall trend", "Summarize insights"]}
            )

        # STEP 4
        step = timer.log("📈 Computing insights")
        if stream_callback:
            stream_callback(f"{step[0]} ({step[1]}s)")

        insights = generate_insights(data)

        chart = generate_chart_safe(data)

        return {
            "insights": insights,
            "chart": chart,
            "data": data,
            "mapping": mapping,
            "sql": sql if "Technical" in profile else None,
            "steps": timer.steps,
            "time": timer.total()
        }

    except:
        return safe_response("Let’s try that differently 👇")