import streamlit as st

from services.faculty_service import(
    create_faculty ,  bulk_create_faculty , get_all_faculty ,fetch_all_faculty,update_faculty_details,remove_faculty, reset_password
)

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

from services.analytics_service import (
    fetch_dashboard_stats,
    fetch_faculty_availability
)

from utils.helper import (
    get_current_slot
)

# ==========================
# CONFIG
# ==========================

st.set_page_config(
    page_title="Faculty Management System",
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
# MAIN APP
# ==========================

else:

    user = st.session_state.user

    faculty_id = user["id"]

    # ----------------------
    # Header
    # ----------------------

    col1, col2 = st.columns([8, 1])

    with col1:

        st.title(
            "Faculty Management System"
        )

        st.write(
            f"Welcome {user['name']}"
        )

        st.caption(
            f"Role: {user['role'].upper()}"
        )

    with col2:

        st.write("")

        if st.button(
            "Logout",
            use_container_width=True
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
                not in st.session_state
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

            # -----------------
            # Attendance
            # -----------------

            if not attendance_done:

                st.subheader(
                    "Today's Attendance"
                )

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "Present",
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

                            st.rerun()

                with col2:

                    if st.button(
                        "Absent",
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

                            st.success(
                                "Marked Absent"
                            )

                            st.rerun()

            # -----------------
            # Schedule Form
            # -----------------

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

        # ==================================
        # DASHBOARD TAB
        # ==================================

        with dashboard_tab:

            st.subheader(
                "Dean Dashboard"
            )

            stats = (
                fetch_dashboard_stats()
            )

            col1, col2, col3 = (
                st.columns(3)
            )

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

            st.markdown("---")

            st.subheader(
                "Quick Insights"
            )

            insight_col1, insight_col2 = (
                st.columns(2)
            )

            with insight_col1:

                st.info(
                    "Faculty who have not marked attendance "
                    "can be monitored here later."
                )

            with insight_col2:

                st.info(
                    "Weekly teaching analytics "
                    "coming soon."
                )

        # ==================================
        # AVAILABILITY TAB
        # ==================================

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

            reverse_slot_map = {
                value: key
                for key, value
                in slot_options.items()
            }

            view_mode = st.radio(
                "View Mode",
                [
                    "Current Slot",
                    "Manual Selection"
                ],
                horizontal=True
            )

            if (
                view_mode
                == "Current Slot"
            ):

                slot_number = (
                    get_current_slot()
                )

                if slot_number:

                    st.success(
                        f"Current Slot: "
                        f"{reverse_slot_map[slot_number]}"
                    )

                else:

                    st.warning(
                        "Outside College Hours"
                    )

                    st.stop()

            else:

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

            faculty_data = (
                fetch_faculty_availability(
                    slot_number
                )
            )

            teaching = []
            available = []

            for row in faculty_data:

                (
                    name,
                    task_type,
                    department,
                    academic_year,
                    topic
                ) = row

                if (
                    task_type
                    == "Teaching"
                ):

                    teaching.append({
                        "name": name,
                        "department":
                        department,
                        "year":
                        academic_year,
                        "topic":
                        topic
                    })

                else:

                    available.append({
                        "name": name,
                        "task":
                        task_type
                    })

            col1, col2 = st.columns(2)

            with col1:

                st.subheader(
                    "Teaching Faculty"
                )

                if teaching:

                    for teacher in teaching:

                        st.info(
                            f"""
**{teacher['name']}**

Department:
{teacher['department']}

Year:
{teacher['year']}

Topic:
{teacher['topic']}
"""
                        )

                else:

                    st.write(
                        "No faculty teaching"
                    )

            with col2:

                st.subheader(
                    "Available Faculty"
                )

                if available:

                    for faculty in available:

                        st.success(
                            f"""
{faculty['name']}

Task:
{faculty['task']}
"""
                        )

                else:

                    st.write(
                        "No faculty available"
                    )

        # ==================================
        # REPORTS TAB
        # ==================================

        with reports_tab:

            st.subheader(
                "Reports"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.button(
                    "Weekly Teaching Hours",
                    use_container_width=True
                )

                st.button(
                    "Attendance Summary",
                    use_container_width=True
                )

            with col2:

                st.button(
                    "Most Active Faculty",
                    use_container_width=True
                )

                st.button(
                    "Faculty Missing Attendance",
                    use_container_width=True
                )

            st.info(
                "Reports backend will be connected next."
            )

        # ==================================
        # SETTINGS TAB
        # ==================================

        with settings_tab:

            (
                add_tab,
                bulk_tab,
                faculty_tab,
                semester_tab
            ) = st.tabs([

                "Add Faculty",
                "Bulk Upload",
                "Faculty List",
                "Semester"
            ])

            # ====================
            # SINGLE FACULTY
            # ====================

            with add_tab:

                st.subheader(
                    "Add New Faculty"
                )

                from services.faculty_service import (
                    create_faculty
                )

                employee_id = (
                    st.text_input(
                        "Employee ID"
                    )
                )

                full_name = (
                    st.text_input(
                        "Full Name"
                    )
                )

                email = (
                    st.text_input(
                        "Email"
                    )
                )

                password = (
                    st.text_input(
                        "Temporary Password",
                        type="password"
                    )
                )

                department = (
                    st.selectbox(
                        "Department",
                        [
                            "CSE",
                            "AI&ML",
                            "Cyber Security",
                            "BCA"
                        ]
                    )
                )

                skills = (
                    st.text_area(
                        "Skills"
                    )
                )

                if st.button(
                    "Create Faculty Account",
                    use_container_width=True
                ):

                    success = (
                        create_faculty(
                            employee_id,
                            full_name,
                            email,
                            password,
                            department,
                            skills
                        )
                    )

                    if success:

                        st.success(
                            "Faculty created successfully!"
                        )

                    else:

                        st.error(
                            "Faculty creation failed"
                        )

            # ====================
            # BULK UPLOAD
            # ====================

            with bulk_tab:

                st.subheader(
                    "Bulk Upload Faculty"
                )

                st.info(
                    """
        CSV Format:

        employee_id,
        full_name,
        email,
        department,
        skills
        """
                )

                uploaded_file = (
                    st.file_uploader(
                        "Upload CSV",
                        type=["csv"]
                    )
                )

                if uploaded_file:

                    from services.faculty_service import (
                        bulk_create_faculty
                    )

                    if st.button(
                        "Upload Faculty",
                        use_container_width=True
                    ):

                        success, credentials_df = (
                            bulk_create_faculty(
                                uploaded_file
                            )
                        )

                        if success:

                            st.success(
                                "Faculty uploaded successfully!"
                            )

                            csv = (
                                credentials_df
                                .to_csv(
                                    index=False
                                )
                            )

                            st.download_button(
                                "Download Credentials",
                                csv,
                                file_name=
                                "faculty_credentials.csv",
                                mime=
                                "text/csv"
                            )

                        else:

                            st.error(
                                "Upload failed"
                            )

            # ====================
            # FACULTY LIST
            # ====================

            with faculty_tab:

                st.subheader(
                    "Faculty List"
                )

                faculty_data = (
                    fetch_all_faculty()
                )

                search_query = st.text_input(
                    "Search Faculty"
                )

                filtered_data = []

                for faculty in faculty_data:

                    (
                        faculty_id,
                        employee_id,
                        full_name,
                        email,
                        department,
                        skills
                    ) = faculty

                    faculty_text = (
                        f"{employee_id} "
                        f"{full_name} "
                        f"{email} "
                        f"{department}"
                    ).lower()

                    if (
                        search_query.lower()
                        in faculty_text
                    ):

                        filtered_data.append(
                            faculty
                        )

                st.write(
                    f"Total Faculty: "
                    f"{len(filtered_data)}"
                )

                for faculty in filtered_data:

                    (
                        faculty_id,
                        employee_id,
                        full_name,
                        email,
                        department,
                        skills
                    ) = faculty

                    with st.expander(
                        f"{full_name} "
                        f"({employee_id})"
                    ):

                        updated_name = (
                            st.text_input(
                                "Name",
                                value=full_name,
                                key=
                                f"name_{faculty_id}"
                            )
                        )

                        updated_email = (
                            st.text_input(
                                "Email",
                                value=email,
                                key=
                                f"email_{faculty_id}"
                            )
                        )

                        department_options = [
                            "CSE",
                            "AI&ML",
                            "Cyber Security",
                            "BCA"
                        ]

                        # fallback if DB value mismatches
                        if department in department_options:

                            department_index = (
                                department_options.index(
                                    department
                                )
                            )

                        else:

                            department_index = 0

                        updated_department = (
                            st.selectbox(
                                "Department",
                                department_options,
                                index=department_index,
                                key=f"dept_{faculty_id}"
                            )
                        )

                        updated_skills = (
                            st.text_area(
                                "Skills",
                                value=skills,
                                key=
                                f"skills_{faculty_id}"
                            )
                        )

                        col1, col2, col3 = (
                            st.columns(3)
                        )

                        with col1:

                            if st.button(
                                "Update",
                                key=
                                f"update_{faculty_id}"
                            ):

                                success = (
                                    update_faculty_details(
                                        faculty_id,
                                        updated_name,
                                        updated_email,
                                        updated_department,
                                        updated_skills
                                    )
                                )

                                if success:

                                    st.success(
                                        "Updated!"
                                    )

                                    st.rerun()

                        with col2:

                            if st.button(
                                "Reset Password",
                                key=
                                f"reset_{faculty_id}"
                            ):

                                (
                                    success,
                                    new_password
                                ) = (
                                    reset_password(
                                        faculty_id,
                                        updated_department
                                    )
                                )

                                if success:

                                    st.success(
                                        f"New Password: "
                                        f"{new_password}"
                                    )

                        with col3:

                            if st.button(
                                "Delete Faculty",
                                key=
                                f"delete_{faculty_id}"
                            ):

                                success = (
                                    remove_faculty(
                                        faculty_id
                                    )
                                )

                                if success:

                                    st.success(
                                        "Faculty deleted"
                                    )

                                    st.rerun()

            # ====================
            # SEMESTER
            # ====================

            with semester_tab:

                st.subheader(
                    "Semester Settings"
                )

                from services.semester_service import (
                    fetch_semesters,
                    fetch_active_semester,
                    change_semester,
                    start_new_semester
                )

                active_semester = (
                    fetch_active_semester()
                )

                st.success(
                    f"Active Semester: "
                    f"{active_semester}"
                )

                semesters = (
                    fetch_semesters()
                )

                semester_map = {}

                for semester in semesters:

                    (
                        semester_id,
                        semester_name,
                        start_date,
                        end_date,
                        is_active
                    ) = semester

                    semester_map[
                        semester_name
                    ] = semester_id

                selected_semester = (
                    st.selectbox(
                        "Choose Semester",
                        list(
                            semester_map.keys()
                        )
                    )
                )

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "Change Active Semester",
                        use_container_width=True
                    ):

                        success = (
                            change_semester(
                                semester_map[
                                    selected_semester
                                ]
                            )
                        )

                        if success:

                            st.success(
                                "Semester Updated"
                            )

                            st.rerun()
                        else :
                            st.error(
                                "Try Again!"
                            )

                            st.rerun()

                with col2:
                    
                    

                    # ==========================
                    # START NEW SEMESTER POPUP
                    # ==========================

                    @st.dialog(
                        "Start New Semester"
                    )
                    def semester_reset_popup():

                        st.warning(
                            """
                    This action will:

                    • Delete attendance records

                    • Delete faculty daily schedules

                    • Reset semester activity data

                    Faculty accounts will remain.
                    """
                        )

                        new_semester_name = (
                            st.text_input(
                                "New Semester Name",
                                placeholder=
                                "Odd Semester 2027"
                            )
                        )

                        confirm_reset = (
                            st.checkbox(
                                "I understand this action "
                                "cannot be undone"
                            )
                        )

                        col1, col2 = st.columns(2)

                        with col1:

                            if st.button(
                                "Cancel",
                                use_container_width=True
                            ):

                                st.rerun()

                        with col2:

                            if st.button(
                                "Agree & Continue",
                                use_container_width=True
                            ):

                                if not (
                                    new_semester_name
                                ):

                                    st.error(
                                        "Enter semester name"
                                    )

                                elif not (
                                    confirm_reset
                                ):

                                    st.error(
                                        "Please confirm reset"
                                    )

                                else:

                                    from services.semester_service import ( initialize_new_semester ) 
                                    
                                    success = ( initialize_new_semester( new_semester_name ) )

                                    if success:

                                        st.success(
                                            "Semester reset completed"
                                        )

                                        st.rerun()
                                        st.markdown("---")

                    if st.button(
                        "Start New Semester",
                        use_container_width=True
                    ):

                        semester_reset_popup()


