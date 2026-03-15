import streamlit as st
import pandas as pd
from agent import run_agent
from guardrails import validate_query
import sys
import os

sys.path.append(os.path.dirname(__file__))

st.title("AI Data Analyst")

persona = st.selectbox(
    "User Profile",
    ["Technical", "Business"]
)

file = st.file_uploader(
    "Upload Excel or CSV",
    type=["csv", "xlsx"]
)

if file:

    if file.name.endswith("xlsx"):
        df = pd.read_excel(file)
    else:
        df = pd.read_csv(file)

    st.success("Dataset Loaded")

    st.subheader("Dataset Preview")
    st.dataframe(df.sample(8))

    st.subheader("Dataset Info")
    schema_df = df.dtypes.reset_index()
    schema_df.columns = ["Column", "Data Type"]

    st.dataframe(schema_df)

    st.write("Columns:", list(df.columns))
    st.write("Rows:", len(df))

    st.subheader("Example Questions")

    examples = [
        "What is the total revenue?",
        "Show average sales by region",
        "Plot sales distribution",
        "Which variable correlates with revenue?",
        "Why did sales decrease?",
        "What trends exist in the dataset?"
    ]

    for q in examples:
        if st.button(q):
            st.session_state["query"] = q

    query = st.text_input(
        "Ask a question",
        value=st.session_state.get("query", "")
    )

    if st.button("Run"):

        try:

            validate_query(query)

            result = run_agent(query, df, persona)

            if hasattr(result, "figure"):
                st.pyplot(result)

            elif str(type(result)).startswith("<class 'matplotlib"):
                st.pyplot(result)

            else:
                st.write(result)

        except Exception as e:

            st.error(str(e))