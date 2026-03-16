import streamlit as st
import pandas as pd

from agent import run_agent
from intelligence_engine import embed_columns
from data_intelligence import analyze_dataset
from analytics_engine import discover_highlevel_insights
from utilities import validate_query

st.title("AI Data Analyst Copilot")

persona = st.selectbox(
    "User Profile",
    ["Business","Technical"]
)

file = st.file_uploader(
    "Upload dataset",
    ["csv","xlsx"]
)

if file:

    if file.name.endswith("xlsx"):
        df = pd.read_excel(file)
    else:
        df = pd.read_csv(file)

    df.columns = df.columns.str.lower().str.replace(" ","_")

    st.success("Dataset Loaded")

    embeddings = embed_columns(df.columns)

    profile = analyze_dataset(df)

    st.markdown("## Automatic Insights")

    insights = discover_highlevel_insights(df,profile)

    for i in insights:

        st.markdown(f"### {i['title']}")

        st.markdown(i["description"])

        st.dataframe(i["evidence"])

    query = st.chat_input("Ask about your dataset")

    if query:

        validate_query(query)

        with st.chat_message("user"):
            st.markdown(query)

        status = st.status("Processing Query",expanded=True)

        status.write("Understanding query")
        status.write("Classifying intent")
        status.write("Mapping dataset columns")

        result = run_agent(query,df,persona,embeddings)

        status.write("Running analytics")
        status.update(label="Analysis Complete",state="complete")

        with st.chat_message("assistant"):

            st.markdown(result["insight"])

            st.dataframe(result["data"])

            st.markdown("### Execution Trace")

            for s in result["steps"]:
                st.markdown(f"- {s}")