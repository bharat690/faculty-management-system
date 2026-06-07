import streamlit as st

from services.auth_service import (
    login_user
)

from utils.session_manager import (
    initialize_session,
    login,
    logout
)

st.set_page_config(
    page_title="Faculty Management System",
    layout="wide"
)

initialize_session()


def show_login_page():

    st.title(
        "Faculty Management System"
    )

    st.subheader("Login")

    email = st.text_input(
        "Email"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        user = login_user(
            email,
            password
        )

        if user:

            login(user)

            st.success(
                "Login successful!"
            )

            st.rerun()

        else:
            st.error(
                "Invalid credentials"
            )


def show_dashboard():

    user = st.session_state.user

    st.sidebar.write(
        f"Welcome {user['name']}"
    )

    st.sidebar.write(
        f"Role: {user['role']}"
    )

    if st.sidebar.button(
        "Logout"
    ):
        logout()
        st.rerun()

    if user["role"] == "dean":

        st.switch_page(
            "pages/2_Dean_Dashboard.py"
        )

    elif user["role"] == "faculty":

        st.switch_page(
            "pages/1_Faculty_Dashboard.py"
        )
    user = st.session_state.user

    st.sidebar.write(
        f"Welcome {user['name']}"
    )

    st.sidebar.write(
        f"Role: {user['role']}"
    )

    if st.sidebar.button(
        "Logout"
    ):
        logout()
        st.rerun()

    if user["role"] == "dean":

        st.title(
            "Dean Dashboard"
        )

    elif user["role"] == "faculty":

        st.title(
            "Faculty Dashboard"
        )


if not st.session_state.logged_in:
    show_login_page()
else:
    show_dashboard()