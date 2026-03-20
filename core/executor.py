import time

from core.cache import get_dataframe
from core.sql_engine import generate_sql, execute_sql
from core.role_manager import format_response
from core.context_manager import update_context
from core.llm_explainer import generate_explanation

from analytics.insight_engine import generate_insights
from analytics.root_cause_engine import discover_root_cause


def execute_query(query, role):
    df = get_dataframe()

    start = time.time()

    context = update_context(query)

    sql = generate_sql(query)
    result_df = execute_sql(df, sql)

    insights = generate_insights(result_df)
    root_cause = discover_root_cause(df)

    # LLM EXPLANATION 
    explanation = None
    if result_df is not None:
        explanation = generate_explanation(
            data=result_df.to_dict(orient="records"),
            insights=insights,
            context=context,
            role=role   
        )

    response = format_response(
        role=role,
        df_result=result_df,
        sql=sql,
        insights=insights,
        root_cause=root_cause
    )

    response["explanation"] = explanation
    response["context"] = context
    response["execution_time"] = round(time.time() - start, 3)

    return response