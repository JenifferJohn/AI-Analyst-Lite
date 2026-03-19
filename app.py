import streamlit as st
import pandas as pd
from agent import run_agent

st.title("AI Analyst Chatbot")

profile = st.selectbox(
    "User Type",
    ["Non-Technical Manager", "Technical Manager"]
)

file = st.file_uploader("Upload Excel", type=["xlsx"])

if file:
    df = pd.read_excel(file)
    st.session_state["df"] = df
    st.write("### Columns:", df.columns.tolist())

query = st.chat_input("Ask your question...")

def stream_callback(msg):
    st.write(msg)

if query:

    result = run_agent(query, profile)

    # 🔹 Clarification Flow
    if result.get("clarification"):

        st.warning(result["message"])

        selections = {}

        for term, options in result["mapping"].items():
            if options:
                selections[term] = st.selectbox(
                    f"What do you mean by '{term}'?",
                    options,
                    key=term
                )

        if st.button("Confirm"):
            result = run_agent(query, profile, resolved=selections)

    # 🔹 Final Output
    if result.get("insights"):
        st.write("### Insights")
        st.write(result["insights"])

    if result.get("chart"):
        st.pyplot(result["chart"])

    st.write("Time:", result.get("time", 0))