import duckdb
from core.context_manager import get_context


def generate_sql(query: str):
    ctx = get_context()

    metric = ctx["metric"]
    dim = ctx["dimension"]
    time_filter = ctx["time_filter"]

    if metric is None:
        return None

    base_query = "SELECT "

    if dim:
        base_query += f"{dim}, "

    base_query += f'SUM("{metric}") as sales FROM df'

    where_clause = ""

    if time_filter == "last_3_months":
        where_clause = """
        WHERE Month >= (SELECT MAX(Month) - INTERVAL '3 months' FROM df)
        """

    group_clause = f" GROUP BY {dim}" if dim else ""

    final_query = f"""
    {base_query}
    {where_clause}
    {group_clause}
    """

    return final_query


def execute_sql(df, sql):
    if sql is None:
        return None

    return duckdb.query(sql).to_df()