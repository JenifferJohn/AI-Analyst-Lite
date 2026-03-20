def format_response(role, df_result, sql, insights, root_cause):
    if role == "non_technical":
        return {
            "summary": insights,
            "data": df_result.to_dict(orient="records") if df_result is not None else None
        }

    if role == "technical":
        return {
            "sql": sql,
            "data": df_result.to_dict(orient="records") if df_result is not None else None,
            "insights": insights,
            "root_cause": root_cause
        }