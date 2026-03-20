import streamlit as st
import pandas as pd
import time

from core.cache import set_dataframe
from core.executor import execute_query
from analytics.chart_generator import generate_chart
from guardrails.input_guardrail import validate_user_query
from guardrails.output_guardrail import validate_output


st.set_page_config(page_title="AI Analyst", layout="wide")

st.title("AI Analyst Chatbot")


# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "df_loaded" not in st.session_state:
    st.session_state.df_loaded = False


# Sidebar
role = st.sidebar.selectbox(
    "User Type",
    ["non_technical", "technical"]
)

uploaded_file = st.sidebar.file_uploader("Upload Excel", type=["xlsx"])


@st.cache_data
def load_data(file):
    return pd.read_excel(file)


# Load data
if uploaded_file and not st.session_state.df_loaded:
    df = load_data(uploaded_file)
    set_dataframe(df)
    st.session_state.df_loaded = True
    st.success("✅ Data loaded successfully")


# Chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# Chat input
if prompt := st.chat_input("Ask your data question..."):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        try:
            validate_user_query(prompt)

            status = st.empty()

            status.info("Understanding context...")
            time.sleep(0.2)

            status.info("Generating SQL...")
            time.sleep(0.2)

            start = time.time()

            status.info("Executing query...")
            result = execute_query(prompt, role)

            status.info("Validating output...")
            time.sleep(0.2)

            result = validate_output(result)

            end = time.time()
            status.empty()

            # Result
            st.subheader("Result")
            st.json(result)

            # KPI
            if result.get("kpis"):
                st.subheader("KPI Summary")
                st.json(result["kpis"])

            # Explanation
            if result.get("explanation"):
                st.subheader("Business Narrative")
                st.write(result["explanation"])

            # Context
            st.subheader("Context Used")
            st.json(result.get("context", {}))

            # Chart
            if "data" in result and result["data"]:
                chart_df = pd.DataFrame(result["data"])
                st.subheader("📊 Visualization")
                generate_chart(chart_df)

            st.success(f"⏱ Completed in {round(end - start, 3)} sec")

            st.session_state.messages.append({
                "role": "assistant",
                "content": str(result)
            })

        except Exception as e:
            st.error(str(e))