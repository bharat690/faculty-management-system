import streamlit as st

from services.attendance_service import (
    attendance_already_marked,
    submit_attendance
)

from services.schedule_service import (
    activity_already_submitted
)

from components.schedule_form import (
    render_schedule_form
)

from utils.session_manager import (
    initialize_session
)


# ==========================
# Session Protection
# ==========================

initialize_session()

if not st.session_state.logged_in:
    st.switch_page("app.py")


# ==========================
# User Validation
# ==========================

user = st.session_state.get(
    "user"
)

if not user:
    st.switch_page("app.py")


faculty_id = user["id"]


# ==========================
# Page UI
# ==========================

st.title(
    "Faculty Dashboard"
)

st.write(
    f"Welcome {user['name']}"
)


# ==========================
# Session Defaults
# ==========================

if "attendance_done" not in st.session_state:

    st.session_state.attendance_done = (
        attendance_already_marked(
            faculty_id
        )
    )

if "show_schedule" not in st.session_state:

    st.session_state.show_schedule = False


attendance_done = (
    st.session_state
    .attendance_done
)

activity_done = (
    activity_already_submitted(
        faculty_id
    )
)


# ==========================
# Attendance Section
# ==========================

if not attendance_done:

    st.subheader(
        "Mark Today's Attendance"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "✅ Present",
            use_container_width=True
        ):

            success = (
                submit_attendance(
                    faculty_id,
                    "present"
                )
            )

            if success:

                st.session_state[
                    "attendance_done"
                ] = True

                st.session_state[
                    "show_schedule"
                ] = True

                st.rerun()

    with col2:

        if st.button(
            "❌ Absent",
            use_container_width=True
        ):

            success = (
                submit_attendance(
                    faculty_id,
                    "absent"
                )
            )

            if success:

                st.session_state[
                    "attendance_done"
                ] = True

                st.rerun()


# ==========================
# Schedule Section
# ==========================

elif (
    attendance_done
    and not activity_done
):

    st.success(
        "Attendance marked"
    )

    if not st.session_state.get(
        "show_schedule",
        False
    ):

        if st.button(
            "Open Today's Schedule",
            use_container_width=True
        ):

            st.session_state[
                "show_schedule"
            ] = True

            st.rerun()

    else:

        render_schedule_form(
            faculty_id
        )


# ==========================
# Already Submitted
# ==========================

else:

    st.success(
        "Today's activity already submitted"
    )