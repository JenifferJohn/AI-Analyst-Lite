import duckdb
import pandas as pd
import streamlit as st

conn = duckdb.connect()

def load_data():
    df = st.session_state.get("df")
    if df is not None:
        conn.execute("CREATE OR REPLACE TABLE data AS SELECT * FROM df")

def get_schema():
    load_data()
    return conn.execute("DESCRIBE data").fetchdf().to_string()

def get_column_info():
    df = st.session_state.get("df")
    info = {}

    for col in df.columns:
        info[col] = {
            "type": str(df[col].dtype),
            "sample": df[col].dropna().head(3).tolist()
        }

    return info

def validate_sql(sql):
    try:
        if not sql.lower().startswith("select"):
            return False, "Only SELECT allowed"
        conn.execute(f"EXPLAIN {sql}")
        return True, ""
    except:
        return False, "Invalid SQL"

def run_query(sql):
    return conn.execute(sql).df()