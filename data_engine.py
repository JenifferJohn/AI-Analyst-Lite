import duckdb
import streamlit as st

conn = duckdb.connect()

def load():
    df = st.session_state.get("df")
    if df is not None:
        conn.execute("CREATE OR REPLACE TABLE data AS SELECT * FROM df")

def get_schema():
    load()
    return conn.execute("DESCRIBE data").fetchdf().to_string()

def get_column_info():
    df = st.session_state["df"]
    return {c: str(df[c].dtype) for c in df.columns}

def validate_sql(sql):
    try:
        if not sql.lower().startswith("select"):
            return False, ""
        conn.execute(f"EXPLAIN {sql}")
        return True, ""
    except:
        return False, ""

def run_query(sql):
    return conn.execute(sql).df()