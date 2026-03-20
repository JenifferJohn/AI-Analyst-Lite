import streamlit as st

def generate_chart(df):
    if df is None or df.empty:
        return

    cols = df.columns

    if "Month" in cols:
        st.line_chart(df.set_index("Month"))

    elif len(cols) == 2:
        st.bar_chart(df.set_index(cols[0]))

    else:
        st.dataframe(df)