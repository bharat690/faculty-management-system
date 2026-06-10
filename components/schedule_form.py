import streamlit as st

from services.schedule_service import (
    submit_daily_schedule
)


def render_schedule_form(
    faculty_id
):

    slot_timings = [
        "9:00–10:00",
        "10:00–11:00",
        "11:00–12:00",
        "12:00–1:00",
        "1:00–2:00",
        "2:00–3:00",
        "3:00–4:00",
        "4:00–5:00"
    ]

    departments = [
        "CSE",
        "AI&ML",
        "Cyber Security",
        "BCA"
    ]

    years = [
        "1st",
        "2nd",
        "3rd",
        "4th"
    ]

    task_options = [
        "Teaching",
        "Office Work",
        "Research",
        "Meeting",
        "Free",
        "Other"
    ]

    st.subheader(
        "Today's Schedule"
    )

    activity_data = []

    # Form prevents rerendering
    # on every interaction
    with st.form(
        "daily_schedule_form"
    ):

        for index, timing in enumerate(
            slot_timings
        ):

            st.markdown("---")

            st.subheader(
                timing
            )

            task_type = (
                st.selectbox(
                    "Task Type",
                    task_options,
                    key=f"task_{index}"
                )
            )

            department = None
            academic_year = None
            topic = ""

            # Only relevant for teaching
            if task_type == "Teaching":

                department = (
                    st.radio(
                        "Department",
                        departments,
                        horizontal=True,
                        key=f"dep_{index}"
                    )
                )

                academic_year = (
                    st.radio(
                        "Year",
                        years,
                        horizontal=True,
                        key=f"year_{index}"
                    )
                )

                topic = (
                    st.text_input(
                        "What will you teach?",
                        placeholder=(
                            "Example: "
                            "Encapsulation, "
                            "DBMS Joins, "
                            "Inheritance"
                        ),
                        key=f"topic_{index}"
                    )
                )

            remarks = (
                st.text_area(
                    "Remarks (Optional)",
                    key=f"remarks_{index}"
                )
            )

            activity_data.append({

                "faculty_id":
                faculty_id,

                "slot_number":
                index + 1,

                "task_type":
                task_type,

                "department":
                department,

                "academic_year":
                academic_year,

                "topic_description":
                topic,

                "remarks":
                remarks
            })

        st.markdown("---")

        submitted = (
            st.form_submit_button(
                "Save Today's Schedule",
                use_container_width=True
            )
        )

        if submitted:

            success = (
                submit_daily_schedule(
                    activity_data
                )
            )

            if success:

                st.success(
                    "Today's schedule saved successfully!"
                )

                st.rerun()

            else:

                st.error(
                    "Failed to save schedule"
                )