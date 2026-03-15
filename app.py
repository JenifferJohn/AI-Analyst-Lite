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
    df.columns = df.columns.str.lower().str.replace(" ", "_")
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

            # clarification flow
            
            if isinstance(result, dict) and result.get("type") == "clarification":
                st.warning(result["message"])
                st.write("Please choose one:")
                
                selected_column = st.selectbox(
                    "Select a column",
                    result["options"]
                )

                if st.button("Confirm Selection"):
                    # rerun agent with selected column
                    result = run_agent(query, df, persona, selected_column)
                    st.write(result)

            # dataframe result
            elif isinstance(result, pd.DataFrame):
                st.dataframe(result)
            # chart result
            elif hasattr(result, "figure"):
                st.pyplot(result)
            # text result
            else:
                st.write(result)