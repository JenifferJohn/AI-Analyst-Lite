import streamlit as st
import pandas as pd

from analysis_agent import generate_analysis_code
from executor import run_analysis
from visualization import render_result
from guardrails import validate_query

st.set_page_config(page_title="AI Analyst")

st.title("AI Analyst Chatbot")

persona = st.selectbox(
    "User Profile",
    ["Technical", "Business"]
)

uploaded_file = st.file_uploader(
    "Upload Excel or CSV",
    type=["csv", "xlsx"]
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if uploaded_file:

    if uploaded_file.name.endswith("xlsx"):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)

    df.columns = df.columns.str.lower().str.replace(" ", "_")

    st.success("Dataset loaded")

    st.subheader("Dataset preview")
    st.dataframe(df.head())

    st.subheader("Columns")

    schema = pd.DataFrame({
        "column": df.columns,
        "datatype": df.dtypes.astype(str)
    })

    st.dataframe(schema)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    query = st.chat_input("Ask a question about your dataset")

    if query:

        st.session_state.messages.append({"role": "user", "content": query})

        with st.chat_message("user"):
            st.markdown(query)

        try:

            validate_query(query)

            code = generate_analysis_code(query, df)

            result = run_analysis(code, df)

            with st.chat_message("assistant"):

                st.markdown("### Analysis Result")

                output = render_result(result)

                if hasattr(output, "figure"):
                    st.pyplot(output)

                elif isinstance(output, pd.DataFrame):
                    st.dataframe(output)

                else:
                    st.markdown(str(output))

            st.session_state.messages.append(
                {"role": "assistant", "content": str(result)}
            )

        except Exception as e:

            with st.chat_message("assistant"):
                st.error(f"Error: {e}")