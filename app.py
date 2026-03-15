import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(__file__))

from agent import run_agent
from guardrails import validate_query

st.title("AI Data Analyst")

persona = st.selectbox(
    "User Profile",
    ["Technical", "Business"]
)

file = st.file_uploader(
    "Upload Excel or CSV",
    type=["csv", "xlsx"]
)

# chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if file:

    if file.name.endswith("xlsx"):
        df = pd.read_excel(file)
    else:
        df = pd.read_csv(file)

    df.columns = df.columns.str.lower().str.replace(" ", "_")

    st.success("Dataset Loaded")

    st.subheader("Dataset Preview")
    st.dataframe(df.sample(min(8, len(df))))

    # display previous chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # chat input
    query = st.chat_input("Ask a question about the dataset")

    if query:

        # show user message
        st.session_state.messages.append({"role": "user", "content": query})

        with st.chat_message("user"):
            st.markdown(query)

        try:

            validate_query(query)

            result = run_agent(query, df, persona)

            with st.chat_message("assistant"):

                # clarification flow
                if isinstance(result, dict) and result.get("type") == "clarification":

                    st.markdown(result["message"])

                    options = result.get("options", [])

                    cols = st.columns(len(options))

                    for i, option in enumerate(options):

                        label = option.replace("_", " ").title()

                        if cols[i].button(label):

                            final_result = run_agent(query, df, persona, option)

                            st.markdown(f"Analyzing **{label}**")

                            if isinstance(final_result, pd.DataFrame):
                                st.dataframe(final_result)
                            else:
                                st.markdown(str(final_result))

                elif isinstance(result, pd.DataFrame):

                    st.dataframe(result)

                elif hasattr(result, "figure"):

                    st.pyplot(result)

                else:

                    st.markdown(str(result))

            st.session_state.messages.append(
                {"role": "assistant", "content": str(result)}
            )

        except Exception as e:

            with st.chat_message("assistant"):
                st.error(f"Error: {e}")