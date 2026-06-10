import streamlit as st

from utils.session_manager import (
    initialize_session
)

initialize_session()

if not st.session_state.logged_in:
    st.switch_page("app.py")

st.title(
    "Dean Dashboard"
)