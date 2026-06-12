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
    fetch_faculty_availability,
    fetch_today_faculty_status
)

from utils.helper import (
    get_current_slot
)

from services.semester_service import (
    fetch_active_semester
)

@st.dialog(
    "Change Password"
)
def change_password_dialog():

    from services.faculty_service import (
        change_password
    )

    current_password = (
        st.text_input(
            "Current Password",
            type="password"
        )
    )

    new_password = (
        st.text_input(
            "New Password",
            type="password"
        )
    )

    confirm_password = (
        st.text_input(
            "Confirm Password",
            type="password"
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
            "Update Password",
            use_container_width=True
        ):

            success, message = (
                change_password(
                    st.session_state
                    .user["id"],

                    current_password,
                    new_password,
                    confirm_password
                )
            )

            if success:

                st.success(
                    message
                )

            else:

                st.error(
                    message
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

        if st.button(
            "Change Password",
            use_container_width=True
        ):

            change_password_dialog()

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
            "Faculty Analytics",
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

            faculty_status = (
                fetch_today_faculty_status()
            )

            active_semester = (
                fetch_active_semester()
            )

            # ==========================
            # FACULTY STATUS LISTS
            # ==========================

            present_faculty = []
            absent_faculty = []
            unmarked_faculty = []

            for name, status in (
                faculty_status
            ):

                if (
                    status
                    == "present"
                ):

                    present_faculty.append(
                        name
                    )

                elif (
                    status
                    == "absent"
                ):

                    absent_faculty.append(
                        name
                    )

                else:

                    unmarked_faculty.append(
                        name
                    )

            # ==========================
            # ATTENDANCE %
            # ==========================

            total_faculty = (
                stats["present"]
                + stats["absent"]
                + stats["unmarked"]
            )

            attendance_percentage = 0

            if total_faculty > 0:

                attendance_percentage = round(
                    (
                        stats["present"]
                        / total_faculty
                    ) * 100
                )

            # ==========================
            # TOP METRICS
            # ==========================

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

            # ==========================
            # QUICK INSIGHTS
            # ==========================

            st.subheader(
                "Quick Insights"
            )

            insight_col1, insight_col2 = (
                st.columns(2)
            )

            # --------------------------
            # Attendance Health
            # --------------------------

            with insight_col1:

                with st.container(
                    border=True
                ):

                    st.markdown(
                        "### Attendance Health"
                    )

                    st.write(
                        f"Attendance Rate: "
                        f"{attendance_percentage}%"
                    )

                    st.progress(
                        attendance_percentage
                    )

                    st.write("")

                    st.selectbox(
                        "Present Faculty",
                        present_faculty
                        if present_faculty
                        else [
                            "No Faculty"
                        ]
                    )

                    st.selectbox(
                        "Absent Faculty",
                        absent_faculty
                        if absent_faculty
                        else [
                            "No Faculty"
                        ]
                    )

                    st.selectbox(
                        "Unmarked Faculty",
                        unmarked_faculty
                        if unmarked_faculty
                        else [
                            "No Faculty"
                        ]
                    )

            # --------------------------
            # Semester + Alerts
            # --------------------------

            with insight_col2:

                with st.container(
                    border=True
                ):

                    st.markdown(
                        "### Current Semester"
                    )

                    st.info(
                        active_semester
                    )

                    st.markdown("---")

                    st.markdown(
                        "### Action Needed"
                    )

                    if (
                        stats["unmarked"]
                        > 0
                    ):

                        st.warning(
                            f"{stats['unmarked']} faculty "
                            f"still need to mark attendance."
                        )

                    else:

                        st.success(
                            "All faculty marked attendance."
                        )

                    if (
                        stats["absent"]
                        > 0
                    ):

                        st.error(
                            f"{stats['absent']} faculty "
                            f"are absent today."
                        )

                    else:

                        st.success(
                            "No faculty absent today."
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

            # ==========================
            # SLOT VIEW TABS
            # ==========================

            current_tab, manual_tab = (
                st.tabs([
                    "Current Slot",
                    "Manual Selection"
                ])
            )

            slot_number = None

            with current_tab:

                current_slot = (
                    get_current_slot()
                )

                if current_slot:

                    slot_number = (
                        current_slot
                    )

                    st.success(
                        f"Current Time Slot: "
                        f"{reverse_slot_map[current_slot]}"
                    )

                else:

                    st.warning(
                        "Outside College Hours"
                    )

            with manual_tab:

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

            st.markdown("---")

            # ==========================
            # FILTERS
            # ==========================

            filter_col1, filter_col2 = (
                st.columns([3, 2])
            )

            with filter_col1:

                selected_department = (
                    st.selectbox(
                        "Department",
                        [
                            "All",
                            "CSE",
                            "AI&ML",
                            "Cyber Security",
                            "BCA"
                        ]
                    )
                )

            with filter_col2:

                only_free = (
                    st.toggle(
                        "Show Only Free Faculty"
                    )
                )

            # ==========================
            # FETCH DATA
            # ==========================

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

                # Department Filter
                if (
                    selected_department
                    != "All"
                    and department
                    != selected_department
                ):

                    continue

                # Free Faculty Filter
                if (
                    only_free
                    and task_type
                    == "Teaching"
                ):

                    continue

                if (
                    task_type
                    == "Teaching"
                ):

                    teaching.append({
                        "name":
                        name,

                        "department":
                        department,

                        "year":
                        academic_year,

                        "topic":
                        topic
                    })

                else:

                    available.append({
                        "name":
                        name,

                        "task":
                        task_type
                    })

            # ==========================
            # FACULTY COLUMNS
            # ==========================

            col1, col2 = st.columns(2)

            # --------------------------
            # Teaching Faculty
            # --------------------------

            with col1:

                st.subheader(
                    " Teaching Faculty"
                )

                if teaching:

                    for teacher in teaching:

                        with st.container(
                            border=True
                        ):

                            st.markdown(
                                f"""
                    ### {teacher['name']}

                    **Department:**  
                    {teacher['department']}

                    **Year:**  
                    {teacher['year']}

                    **Teaching:**  
                    {teacher['topic']}
                    """
                                        )

                else:

                    st.info(
                        "No faculty teaching"
                    )

            # --------------------------
            # Available Faculty
            # --------------------------

            with col2:

                st.subheader(
                    " Available Faculty"
                )

                if available:

                    for faculty in available:

                        with st.container(
                            border=True
                        ):

                            st.markdown(
                                f"""
                            ### {faculty['name']}

                            **Current Status:**  
                            {faculty['task']}
                            """
                            )

                else:

                    st.info(
                        "No faculty available"
                    )

        # ==================================
        # REPORTS TAB
        # ==================================

        with reports_tab:

            st.subheader(
                "Faculty Analytics"
            )

            from services.report_service import (
                fetch_faculty_list,
                fetch_week_summary,
                fetch_month_summary,
                fetch_semester_summary
            )

            faculty_list = (
                fetch_faculty_list()
            )

            if not faculty_list:

                st.warning(
                    "No faculty found"
                )

            else:

                faculty_map = {

                    f"{name} "
                    f"({employee_id})":

                    {
                        "id":
                        faculty_id,

                        "department":
                        department,

                        "employee_id":
                        employee_id
                    }

                    for (
                        faculty_id,
                        employee_id,
                        name,
                        department
                    )

                    in faculty_list
                }

                selected_faculty = (
                    st.selectbox(
                        "Search Faculty",
                        faculty_map.keys()
                    )
                )

                selected_data = (
                    faculty_map[
                        selected_faculty
                    ]
                )

                faculty_id = (
                    selected_data[
                        "id"
                    ]
                )

                # ==================
                # FACULTY HEADER
                # ==================

                st.markdown("---")

                col1, col2, col3 = (
                    st.columns(3)
                )

                with col1:

                    st.write(
                        "Name"
                    )

                    st.info(
                        selected_faculty
                        .split("(")[0]
                    )

                with col2:

                    st.write(
                        "Employee ID"
                    )

                    st.info(
                        selected_data[
                            "employee_id"
                        ]
                    )

                with col3:

                    st.write(
                        "Department"
                    )

                    st.info(
                        selected_data[
                            "department"
                        ]
                    )

                st.markdown("---")

                # ==================
                # SUMMARIES
                # ==================

                week_summary = (
                    fetch_week_summary(
                        faculty_id
                    )
                )

                month_summary = (
                    fetch_month_summary(
                        faculty_id
                    )
                )

                semester_summary = (
                    fetch_semester_summary(
                        faculty_id
                    )
                )

                st.subheader(
                    "Performance Summary"
                )

                week_col, month_col, sem_col = (
                    st.columns(3)
                )

                # ------------------
                # Week
                # ------------------

                with week_col:

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            "### This Week"
                        )

                        st.metric(
                            "Present Days",
                            week_summary[
                                "present_days"
                            ]
                        )

                        st.metric(
                            "Teaching Hours",
                            week_summary[
                                "teaching_hours"
                            ]
                        )

                        st.metric(
                            "Work Hours",
                            week_summary[
                                "work_hours"
                            ]
                        )

                        st.metric(
                            "Free Hours",
                            week_summary[
                                "free_hours"
                            ]
                        )

                # ------------------
                # Month
                # ------------------

                with month_col:

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            "### Last 30 Days"
                        )

                        st.metric(
                            "Present Days",
                            month_summary[
                                "present_days"
                            ]
                        )

                        st.metric(
                            "Teaching Hours",
                            month_summary[
                                "teaching_hours"
                            ]
                        )

                        st.metric(
                            "Work Hours",
                            month_summary[
                                "work_hours"
                            ]
                        )

                        st.metric(
                            "Free Hours",
                            month_summary[
                                "free_hours"
                            ]
                        )

                # ------------------
                # Semester
                # ------------------

                with sem_col:

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            "### Semester"
                        )

                        st.metric(
                            "Present Days",
                            semester_summary[
                                "present_days"
                            ]
                        )

                        st.metric(
                            "Teaching Hours",
                            semester_summary[
                                "teaching_hours"
                            ]
                        )

                        st.metric(
                            "Work Hours",
                            semester_summary[
                                "work_hours"
                            ]
                        )

                        st.metric(
                            "Free Hours",
                            semester_summary[
                                "free_hours"
                            ]
                        )
            from services.report_service import (
                    fetch_weekly_classes,
                    fetch_topics_by_class
            )
            st.markdown("---")

            # ==========================
            # WEEKLY CLASSES
            # ==========================

            st.subheader(
                "Classes Taught This Week"
            )

            weekly_classes = (
                fetch_weekly_classes(
                    faculty_id
                )
            )

            slot_map = {

                1: "9:00–10:00",
                2: "10:00–11:00",
                3: "11:00–12:00",
                4: "12:00–1:00",
                5: "1:00–2:00",
                6: "2:00–3:00",
                7: "3:00–4:00",
                8: "4:00–5:00"
            }

            grouped_classes = {}

            for row in weekly_classes:

                (
                    activity_date,
                    slot_number,
                    department,
                    academic_year,
                    topic
                ) = row

                day_name = (
                    activity_date.strftime(
                        "%A"
                    )
                )

                if (
                    day_name
                    not in
                    grouped_classes
                ):

                    grouped_classes[
                        day_name
                    ] = []

                grouped_classes[
                    day_name
                ].append(
                    f"{slot_map[slot_number]}"
                    f" → "
                    f"{topic or 'No Topic'} "
                    f"({department} "
                    f"{academic_year})"
                )

            if grouped_classes:

                for day, classes in (
                    grouped_classes.items()
                ):

                    with st.expander(
                        day
                    ):

                        for cls in classes:

                            st.write(
                                cls
                            )

            else:

                st.info(
                    "No teaching activity recorded this week."
                )


            st.markdown("---")

            # ==========================
            # TOPICS BY CLASS
            # ==========================

            st.subheader(
                "Topics Taught by Class"
            )

            topics = (
                fetch_topics_by_class(
                    faculty_id
                )
            )

            class_topics = {}

            for row in topics:

                (
                    department,
                    academic_year,
                    topic
                ) = row

                key = (
                    f"{department} "
                    f"- "
                    f"{academic_year}"
                )

                if (
                    key
                    not in
                    class_topics
                ):

                    class_topics[
                        key
                    ] = []

                if (
                    topic
                    and topic
                    not in
                    class_topics[key]
                ):

                    class_topics[
                        key
                    ].append(
                        topic
                    )

            if class_topics:

                for cls, topic_list in (
                    class_topics.items()
                ):

                    with st.expander(
                        cls
                    ):

                        for topic in (
                            topic_list
                        ):

                            st.write(
                                f"• {topic}"
                            )

            else:

                st.info(
                    "No topics available"
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


