import streamlit as st

from services.auth_service import (
    login_user
)

from utils.session_manager import (
    initialize_session,
    login,
    logout
)

from components.schedule_form import (
    render_schedule_form
)

from services.attendance_service import (
    attendance_already_marked,
    submit_attendance
)

from services.schedule_service import (
    activity_already_submitted
)

# ==========================
# CONFIG
# ==========================

st.set_page_config(
    page_title=
    "Faculty Management System",
    layout="wide"
)

initialize_session()


# ==========================
# LOGIN SCREEN
# ==========================

if not st.session_state.logged_in:

    st.title(
        "Faculty Management System"
    )

    st.subheader(
        "Login"
    )

    email = st.text_input(
        "Email"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button(
        "Login",
        use_container_width=True
    ):

        user = login_user(
            email,
            password
        )

        if user:

            login(user)

            st.rerun()

        else:

            st.error(
                "Invalid Credentials"
            )


# ==========================
# LOGGED IN APP
# ==========================

else:

    user = st.session_state.user

    faculty_id = user["id"]

    # ----------------------
    # Header
    # ----------------------

    col1, col2 = st.columns(
        [8, 1]
    )

    with col1:

        st.title(
            "Faculty Management System"
        )

        st.write(
            f"Welcome "
            f"{user['name']}"
        )

    with col2:

        if st.button(
            "Logout"
        ):

            logout()
            st.rerun()

    st.markdown("---")

    # ======================
    # FACULTY VIEW
    # ======================

    if user["role"] == "faculty":

        dashboard_tab = st.tabs([
            "Dashboard"
        ])[0]

        with dashboard_tab:

            if (
                "attendance_done"
                not in
                st.session_state
            ):

                st.session_state[
                    "attendance_done"
                ] = (
                    attendance_already_marked(
                        faculty_id
                    )
                )

            attendance_done = (
                st.session_state
                .attendance_done
            )

            activity_done = (
                activity_already_submitted(
                    faculty_id
                )
            )

            # ----------------
            # Attendance
            # ----------------

            if not attendance_done:

                st.subheader(
                    "Today's Attendance"
                )

                present = st.toggle(
                    "Present"
                )

                if present:

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

                        st.rerun()

            # ----------------
            # Schedule
            # ----------------

            elif (
                attendance_done
                and not activity_done
            ):

                st.success(
                    "Attendance Marked"
                )

                render_schedule_form(
                    faculty_id
                )

            else:

                st.success(
                    "Today's schedule already submitted"
                )

    # ======================
    # DEAN VIEW
    # ======================

    elif user["role"] == "dean":

        (
            dashboard_tab,
            availability_tab,
            reports_tab,
            settings_tab
        ) = st.tabs([

            "Dashboard",
            "Faculty Availability",
            "Reports",
            "Settings"
        ])

        # -----------------
        # Dashboard
        # -----------------

        with dashboard_tab:

            st.subheader(
                "Dean Dashboard"
            )

            from services.analytics_service import (
                fetch_dashboard_stats
            )

            stats = (
                fetch_dashboard_stats()
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Present Today",
                    stats["present"]
                )

            with col2:

                st.metric(
                    "Absent Today",
                    stats["absent"]
                )

            with col3:

                st.metric(
                    "Unmarked",
                    stats["unmarked"]
                )

        # -----------------
        # Availability
        # -----------------

        with availability_tab:

            st.subheader(
                "Faculty Availability"
            )

            slot_options = {
                "9:00–10:00": 1,
                "10:00–11:00": 2,
                "11:00–12:00": 3,
                "12:00–1:00": 4,
                "1:00–2:00": 5,
                "2:00–3:00": 6,
                "3:00–4:00": 7,
                "4:00–5:00": 8
            }

            selected_slot = (
                st.selectbox(
                    "Choose Time Slot",
                    list(
                        slot_options.keys()
                    )
                )
            )

            slot_number = (
                slot_options[
                    selected_slot
                ]
            )

            from services.analytics_service import (
                fetch_faculty_availability
            )

            faculty_data = (
                fetch_faculty_availability(
                    slot_number
                )
            )

            teaching = []
            free = []

            for row in faculty_data:

                (
                    name,
                    task_type,
                    department,
                    year,
                    topic
                ) = row

                if (
                    task_type
                    == "Teaching"
                ):

                    teaching.append(
                        (
                            name,
                            department,
                            year,
                            topic
                        )
                    )

                else:

                    free.append(
                        (
                            name,
                            task_type
                        )
                    )

            # -------------------
            # Teaching Faculty
            # -------------------

            col1, col2 = st.columns(2)

            with col1:

                st.subheader(
                    "Teaching Faculty"
                )

                if teaching:

                    for item in teaching:

                        (
                            name,
                            department,
                            year,
                            topic
                        ) = item

                        st.info(
                            f"""
        {name}

        {department}
        {year} Year

        Topic:
        {topic}
        """
                        )

                else:

                    st.write(
                        "No teaching faculty"
                    )

            # -------------------
            # Free Faculty
            # -------------------

            with col2:

                st.subheader(
                    "Available Faculty"
                )

                if free:

                    for item in free:

                        name, task = item

                        st.success(
                            f"{name} "
                            f"({task})"
                        )

                else:

                    st.write(
                        "No available faculty"
                    )

        # -----------------
        # Reports
        # -----------------

        with reports_tab:

            st.subheader(
                "Reports"
            )

            st.info(
                "Reports section"
            )

        # -----------------
        # Settings
        # -----------------

        with settings_tab:

            st.subheader(
                "Admin Settings"
            )

            st.button(
                "Add Faculty"
            )

            st.button(
                "Change Semester"
            )