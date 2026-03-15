import streamlit as st
import pandas as pd

from core.analytics_engine import run_query, auto_chart, detect_trend
from core.guardrails import suggest_columns
from core.llm_engine import summarize, is_summary_query


st.set_page_config(page_title="AI Excel Analyst", layout="wide")

st.title("AI Analyst for Excel")


@st.cache_data
def load_data(file):

    if file.name.endswith(".csv"):
        return pd.read_csv(file)

    return pd.read_excel(file)


file = st.file_uploader("Upload Excel or CSV", type=["xlsx", "csv"])

if not file:
    st.info("Upload dataset to begin")
    st.stop()


df = load_data(file)


if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = []

if "analysis_memory" not in st.session_state:
    st.session_state.analysis_memory = []


for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])


query = st.chat_input("Ask about your dataset")

if not query:
    st.stop()


st.session_state.messages.append(
    {"role": "user", "content": query}
)


if is_summary_query(query):

    summary = summarize(
        st.session_state.analysis_memory
    )

    with st.chat_message("assistant"):
        st.write(summary)

    st.stop()


suggest = suggest_columns(query, df)

if suggest:

    st.info("Possible columns")

    cols = st.columns(len(suggest))

    for i, c in enumerate(suggest):

        if cols[i].button(c):
            st.rerun()


history = "\n".join(
    st.session_state.history[-5:]
)


success, result = run_query(
    query,
    df,
    history
)


with st.chat_message("assistant"):

    if not success:

        st.warning(result)

    else:

        if result["status"] == "empty":

            st.info(result["message"])

        else:

            data = result["data"]

            if isinstance(data, pd.DataFrame):

                st.dataframe(data)

                chart = auto_chart(data)

                if chart:
                    st.plotly_chart(chart)

                trend = detect_trend(data)

                if trend:
                    st.info(trend)

                st.session_state.analysis_memory.append({
                    "query": query,
                    "preview": str(data.head())
                })

            else:

                st.write(data)


st.session_state.history.append(query)