import streamlit as st

from services.attendance_service import (
    attendance_already_marked,
    submit_attendance
)


st.title("Faculty Dashboard")

user = st.session_state.user

st.write(
    f"Welcome {user['name']}"
)

faculty_id = user["id"]


already_marked = (
    attendance_already_marked(
        faculty_id
    )
)

if already_marked:

    st.success(
        "Attendance already submitted today"
    )

else:

    st.subheader(
        "Mark Today's Attendance"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Present",
            use_container_width=True
        ):

            success = submit_attendance(
                faculty_id,
                "present"
            )

            if success:
                st.success(
                    "Marked Present"
                )
                st.rerun()

    with col2:

        if st.button(
            "Absent",
            use_container_width=True
        ):

            success = submit_attendance(
                faculty_id,
                "absent"
            )

            if success:
                st.success(
                    "Marked Absent"
                )
                st.rerun()