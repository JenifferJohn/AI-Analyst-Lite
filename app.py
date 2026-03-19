import streamlit as st
import pandas as pd

from agent import run_agent
from intelligence_engine import embed_columns
from data_intelligence import analyze_dataset, detect_date_candidates
from analytics_engine import discover_highlevel_insights

st.title("AI Analyst Chatbot")

persona = st.selectbox("Profile", ["Business","Technical"])

file = st.file_uploader("Upload dataset", ["csv","xlsx"])

if file:

    df = pd.read_excel(file) if file.name.endswith("xlsx") else pd.read_csv(file)

    # clean column names
    df.columns = df.columns.str.lower().str.replace("[^a-z0-9]+","_",regex=True)

    # fix numeric columns
    for col in df.columns:
        df[col] = df[col].replace(",", "", regex=True)
        df[col] = pd.to_numeric(df[col], errors="ignore")

    st.success("Dataset Loaded")

    profile = analyze_dataset(df)

    # 🎯 TARGET COLUMN (unchanged)
    target_column = st.selectbox("Select Target Metric", profile["metrics"])

    # ⭐ NEW DATE DETECTION
    st.subheader("Select Time Column")

    date_candidates = detect_date_candidates(df)

    if date_candidates:

        date_column = st.selectbox(
            "Detected Date Columns",
            ["None"] + date_candidates,
            index=1  # auto select first detected
        )

    else:

        st.warning("No date columns detected. Please select manually.")

        date_column = st.selectbox(
            "Select Date Column",
            ["None"] + list(df.columns)
        )

    if date_column == "None":
        date_column = None

    st.info(f"""
Using:
- Target: {target_column}
- Date: {date_column if date_column else "Not selected"}
""")

    emb = embed_columns(df.columns)

    # auto insights using selected columns
    profile["metrics"] = [target_column]

    if date_column:
        profile["time"] = date_column

    st.subheader("Automatic Insights")

    for i in discover_highlevel_insights(df, profile):

        st.markdown(f"### {i['title']}")
        st.write(i["description"])
        st.dataframe(i["evidence"])

    # chatbot
    q = st.chat_input("Ask question")

    if q:

        with st.chat_message("user"):
            st.write(q)

        result = run_agent(
            q,
            df,
            persona,
            emb,
            target_column,
            date_column
        )

        with st.chat_message("assistant"):
            st.write(result["insight"])
            st.dataframe(result["data"])

            st.markdown("### Execution Trace")

            for s in result["steps"]:
                st.write(s)