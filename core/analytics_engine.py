import pandas as pd
import plotly.express as px
import numpy as np

from core.llm_engine import generate_code, fix_code
from core.guardrails import validate_code, normalize_result

MAX_RETRIES=3

def execute_code(code, df):

    local_vars = {
        "df": df,
        "pd": pd,
        "px": px
    }

    try:

        exec(code, {}, local_vars)

        return True, local_vars.get("result")

    except Exception as e:

        return False, str(e)


def run_query(query, df, history):

    code = generate_code(query, df, history)

    for _ in range(MAX_RETRIES):

        valid, reason = validate_code(code)

        if not valid:
            return False, f"Guardrail triggered: {reason}"

        success, result = execute_code(code, df)

        if success:
            return True, normalize_result(result)

        code = fix_code(query, code, result, list(df.columns))

    return False, "Query failed after retries"


def auto_chart(result):

    if not isinstance(result, pd.DataFrame):
        return None

    if len(result.columns) < 2:
        return None

    x = result.columns[0]
    y = result.columns[1]

    if result[y].dtype in ["int64", "float64"]:

        if "date" in x.lower():
            return px.line(result, x=x, y=y)

        if result[x].nunique() < 20:
            return px.bar(result, x=x, y=y)

        return px.scatter(result, x=x, y=y)

    return None


def detect_trend(df):

    if not isinstance(df, pd.DataFrame):
        return None

    numeric = df.select_dtypes(include=np.number)

    if len(numeric.columns) == 0:
        return None

    col = numeric.columns[0]

    vals = numeric[col].values

    if len(vals) < 3:
        return None

    slope = np.polyfit(range(len(vals)), vals, 1)[0]

    if slope > 0:
        return "📈 Upward trend detected"

    if slope < 0:
        return "📉 Downward trend detected"

    return None