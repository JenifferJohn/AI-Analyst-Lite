import streamlit as st

def init_memory():
    if "history" not in st.session_state:
        st.session_state.history = []