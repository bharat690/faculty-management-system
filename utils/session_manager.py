import streamlit as st


def initialize_session():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "user" not in st.session_state:
        st.session_state.user = None


def login(user):

    st.session_state.logged_in = True
    st.session_state.user = user


def logout():

    st.session_state.logged_in = False
    st.session_state.user = None