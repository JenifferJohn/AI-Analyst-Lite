import streamlit as st
import pandas as pd
from agent import run_agent

st.title(" AI Analyst")

# --- SESSION INIT ---
for key in ["query", "clarification", "suggestions"]:
    if key not in st.session_state:
        st.session_state[key] = None

profile = st.selectbox(
    "User Type",
    ["Non-Technical Manager", "Technical Manager"]
)

file = st.file_uploader("Upload Excel", type=["xlsx"])

if file:
    df = pd.read_excel(file)
    st.session_state["df"] = df
    st.write("### Columns:", df.columns.tolist())

    # auto-run first insight
    if not st.session_state.query:
        st.session_state.query = "Summarize key insights"

# --- STREAM OUTPUT ---
output_box = st.empty()

def stream_callback(msg):
    with output_box.container():
        st.write(msg)

# --- USER INPUT ---
user_query = st.chat_input("Ask your question...")

if user_query:
    st.session_state.query = user_query

# --- MAIN EXECUTION ---
if st.session_state.query:

    result = run_agent(
        st.session_state.query,
        profile,
        stream_callback=stream_callback
    )

    # --- CLARIFICATION ---
    if result.get("clarification"):
        st.session_state.clarification = True
        st.session_state.suggestions = result["suggestions"]

    # --- HANDLE CLARIFICATION ---
    if st.session_state.clarification:

        st.warning("Let’s refine your request 👇")

        selections = {}

        for k, v in st.session_state.suggestions.items():
            selections[k] = st.selectbox(f"Select {k}", v)

        if st.button("Confirm Selection"):
            result = run_agent(
                st.session_state.query,
                profile,
                resolved=selections
            )
            st.session_state.clarification = False

    # --- OUTPUT ---
    if result.get("insights"):
        st.write("### 📊 Insights")
        st.write(result["insights"])

    if result.get("chart"):
        st.pyplot(result["chart"])

    # 🔍 DATA EVIDENCE
    if result.get("data") is not None:
        st.write("### 🔍 Data Evidence")
        st.dataframe(result["data"].head(10))

    # ⏱ Timeline
    if result.get("steps"):
        st.write("### ⏱ Execution Summary")
        for step, t in result["steps"]:
            st.write(f"{step} → {t}s")

        st.success(f"✅ Completed in {result['time']}s")

    # 👨‍💻 Technical view
    if "Technical" in profile:
        with st.expander("🔍 Debug Info"):
            st.json(result.get("mapping", {}))
            if result.get("sql"):
                st.code(result["sql"], language="sql")