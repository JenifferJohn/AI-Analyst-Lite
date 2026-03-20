import streamlit as st
import pandas as pd
import time

from core.cache import set_dataframe
from core.executor import execute_query
from core.fast_executor import fast_execute
from analytics.chart_generator import generate_chart
from guardrails.input_guardrail import validate_user_query
from guardrails.output_guardrail import validate_output
from utils.smart_suggestions import generate_smart_questions
from utils.smart_naming import apply_friendly_names, humanize_query


st.set_page_config(page_title="AI Analyst", layout="wide")

st.title("AI Analyst Chatbot")


# -----------------------------
# Session state
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "df_loaded" not in st.session_state:
    st.session_state.df_loaded = False

if "suggested_query" not in st.session_state:
    st.session_state.suggested_query = None


# -----------------------------
# Sidebar
# -----------------------------
role = st.sidebar.selectbox(
    "User Type",
    ["non_technical", "technical"]
)

uploaded_file = st.sidebar.file_uploader("Upload Excel", type=["xlsx"])


@st.cache_data
def load_data(file):
    return pd.read_excel(file)


# -----------------------------
# Load data
# -----------------------------
if uploaded_file and not st.session_state.df_loaded:
    df = load_data(uploaded_file)

    clean_df, col_map = apply_friendly_names(df)

    set_dataframe(df)  # keep original for execution
    st.session_state.df = df
    st.session_state.clean_df = clean_df
    st.session_state.col_map = col_map

    st.session_state.df_loaded = True
    st.success("Data loaded successfully")


# -----------------------------
# Smart Suggestions
# -----------------------------
def set_suggested_query(q):
    st.session_state.suggested_query = q


if st.session_state.get("df_loaded"):

    st.subheader("Smart Suggestions")

    suggestions = generate_smart_questions(st.session_state.df)

    cols = st.columns(2)

    for i, q in enumerate(suggestions):
        cols[i % 2].button(q, on_click=set_suggested_query, args=(q,))


# -----------------------------
# Safety Filter
# -----------------------------
def is_safe_query(query):
    unsafe_keywords = ["why", "predict", "forecast", "recommend", "suggest"]
    return not any(word in query.lower() for word in unsafe_keywords)


# -----------------------------
# Fast Query Router
# -----------------------------
def is_fast_query(query):
    keywords = ["total", "sales", "by", "trend", "growth", "top", "market", "product"]
    return any(k in query.lower() for k in keywords)


# -----------------------------
# Chat History
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# -----------------------------
# Input Source
# -----------------------------
prompt = None

if st.session_state.suggested_query:
    prompt = st.session_state.suggested_query
    st.session_state.suggested_query = None
else:
    prompt = st.chat_input("Ask your data question...")


# -----------------------------
# Execution Flow
# -----------------------------
if prompt:

    display_prompt = humanize_query(prompt, st.session_state.get("col_map", {}))

    st.session_state.messages.append({"role": "user", "content": display_prompt})

    with st.chat_message("user"):
        st.markdown(display_prompt)

    with st.chat_message("assistant"):

        try:
            if not is_safe_query(prompt):
                raise ValueError("Ask a structured data question")

            validate_user_query(prompt)

            status = st.empty()

            status.info("Understanding context...")
            time.sleep(0.2)

            status.info("Routing query...")
            time.sleep(0.1)

            start = time.time()

            df = st.session_state.get("df")

            # -----------------------------
            # FAST PATH
            # -----------------------------
            if is_fast_query(prompt):
                fast_result = fast_execute(prompt, df)
                if fast_result:
                    result = fast_result
                else:
                    status.info("Falling back to full engine...")
                    result = execute_query(prompt, role)
            else:
                result = execute_query(prompt, role)

            status.info("Validating output...")
            time.sleep(0.2)

            result = validate_output(result)

            end = time.time()
            status.empty()

            # -----------------------------
            # RESULT DISPLAY
            # -----------------------------
            st.subheader("Result")
            st.json(result)

            if result.get("kpis"):
                st.subheader("KPI Summary")
                st.json(result["kpis"])

            if result.get("explanation"):
                st.subheader("Business Narrative")
                st.write(result["explanation"])

            st.subheader("Context Used")
            st.json(result.get("context", {}))

            if "data" in result and result["data"]:
                chart_df = pd.DataFrame(result["data"])
                st.subheader("Visualization")
                generate_chart(chart_df)

            st.write(f"Completed in {round(end - start, 3)} sec")

            st.session_state.messages.append({
                "role": "assistant",
                "content": str(result)
            })

        except Exception as e:
            st.error(str(e))