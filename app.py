import streamlit as st
import pandas as pd

from agent import run_agent
from intelligence_engine import embed_columns
from data_intelligence import analyze_dataset, detect_date_candidates,detect_target_candidates 
from analytics_engine import discover_highlevel_insights
from utilities import validate_query

st.title("AI Analyst Chatbot")

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
    
    # fix numeric types
    for col in df.columns:
        df[col] = df[col].replace(",", "", regex=True)
        df[col] = pd.to_numeric(df[col], errors="ignore")

    st.success("Dataset Loaded")  

    profile = analyze_dataset(df)

    st.write("Detected Metrics:", profile["metrics"])
    st.write("Detected Dimensions:", profile["dimensions"])
    st.write("Detected Time Column:", profile["time"])
    
    #detect target column
    target_candidates = detect_target_candidates(df)

    default_target = (
        target_candidates[0]
        if target_candidates
        else (profile["metrics"][0] if profile["metrics"] else df.columns[0])
    )

    st.subheader("Select Target Column")

    target_column = st.selectbox(
        "Target Metric",
        df.columns,
        index=list(df.columns).index(default_target)
    )


    date_candidates = detect_date_candidates(df)

    st.subheader("Select Time Column")

    if date_candidates:

        date_column = st.selectbox(
            "Detected Date Columns",
            ["None"] + date_candidates,
            index=1
        )

    else:

        st.warning("No date columns detected. Please select manually.")

        date_column = st.selectbox(
            "Select Date Column",
            ["None"] + list(df.columns)
        )

    if date_column == "None":
        date_column = None

    
    # fix numeric types
    for col in df.columns:
        df[col] = df[col].replace(",", "", regex=True)
        df[col] = pd.to_numeric(df[col], errors="ignore")

    st.success("Dataset Loaded")  

    profile = analyze_dataset(df)

    st.write("Detected Metrics:", profile["metrics"])
    st.write("Detected Dimensions:", profile["dimensions"])
    st.write("Detected Time Column:", profile["time"])
    
    embeddings = embed_columns(df.columns)

    profile = analyze_dataset(df)

    st.markdown("## Automatic Insights")

    insights = discover_highlevel_insights(df, profile, target_column)

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
    