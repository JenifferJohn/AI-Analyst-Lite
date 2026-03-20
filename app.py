import streamlit as st
import pandas as pd
import time

from core.cache import set_dataframe
from core.executor import execute_query
from analytics.chart_generator import generate_chart
from guardrails.input_guardrail import validate_user_query
from guardrails.output_guardrail import validate_output


# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="AI Analyst", layout="wide")

st.title("AI Analyst")


# -------------------------------
# SESSION STATE
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "df_loaded" not in st.session_state:
    st.session_state.df_loaded = False


# -------------------------------
# SIDEBAR
# -------------------------------
role = st.sidebar.selectbox(
    "User Type",
    ["non_technical", "technical"]
)

uploaded_file = st.sidebar.file_uploader("Upload Excel", type=["xlsx"])


# -------------------------------
# DATA LOADER
# -------------------------------
@st.cache_data
def load_data(file):
    return pd.read_excel(file)


# -------------------------------
# LOAD DATA
# -------------------------------
if uploaded_file and not st.session_state.df_loaded:
    df = load_data(uploaded_file)
    set_dataframe(df)
    st.session_state.df_loaded = True
    st.success("Data loaded successfully and cached")


# -------------------------------
# DISPLAY CHAT HISTORY
# -------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# -------------------------------
# CHAT INPUT
# -------------------------------
if prompt := st.chat_input("Ask your data question..."):

    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # -------------------------------
    # ASSISTANT RESPONSE
    # -------------------------------
    with st.chat_message("assistant"):

        try:
            # INPUT GUARDRAIL
            validate_user_query(prompt)

            # STATUS UPDATES (REAL-TIME FEEL)
            status = st.empty()

            status.info("Understanding context...")
            time.sleep(0.2)

            status.info("Generating SQL from context...")
            time.sleep(0.2)

            start = time.time()

            status.info("Executing query on full dataset...")
            result = execute_query(prompt, role)

            status.info(" Validating output...")
            time.sleep(0.2)

            # OUTPUT GUARDRAIL
            result = validate_output(result)

            end = time.time()

            status.empty()

            # -------------------------------
            # SHOW RESULT (RAW)
            # -------------------------------
            st.subheader("📦 Result")
            st.json(result)

            # -------------------------------
            # LLM EXPLANATION (OLLAMA)
            # -------------------------------
            if result.get("explanation"):
                st.subheader("Explanation (LLM Generated)")
                st.write(result["explanation"])

            # -------------------------------
            # CONTEXT (TRANSPARENCY)
            # -------------------------------
            st.subheader("🧠 Context Used")
            st.json(result.get("context", {}))

            # -------------------------------
            # CHART GENERATION
            # -------------------------------
            if "data" in result and result["data"]:
                chart_df = pd.DataFrame(result["data"])
                st.subheader("Visualization")
                generate_chart(chart_df)

            # -------------------------------
            # EXECUTION TIME
            # -------------------------------
            st.success(f"⏱ Completed in {round(end - start, 3)} sec")

            # Save assistant message
            st.session_state.messages.append({
                "role": "assistant",
                "content": str(result)
            })

        except Exception as e:
            st.error(str(e))