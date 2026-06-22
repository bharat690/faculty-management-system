import streamlit as st
from datetime import date, timedelta

from services.schedule_service import (
    submit_daily_schedule
)


# ==========================================
# DIALOG: Step 2 Confirmation
# ==========================================

@st.dialog("Confirm Schedule Submission")
def _show_save_dialog():
    
    data = st.session_state.get("pending_schedule_data", [])
    
    st.write("Please review your schedule before confirming:")
    
    for item in data:
        slot = item["slot_number"]
        task = item["task_type"]
        
        if task == "Teaching":
            st.info(
                f"**Slot {slot}:** {task} → {item['topic_description'] or 'No Topic'} "
                f"({item['department']} - {item['academic_year']})"
            )
        else:
            st.write(f"**Slot {slot}:** {task}")
            
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Cancel", use_container_width=True):
            if "show_save_dialog" in st.session_state:
                del st.session_state["show_save_dialog"]
            st.rerun()
            
    with col2:
        if st.button("Confirm & Save", type="primary", use_container_width=True):
            success = submit_daily_schedule(data)
            
            if success:
                st.success("Schedule saved successfully!")
                if "show_save_dialog" in st.session_state:
                    del st.session_state["show_save_dialog"]
                st.rerun()
            else:
                st.error("Failed to save schedule")


# ==========================================
# MAIN FORM: Fragment (No Flash)
# ==========================================

@st.fragment
def render_schedule_form(
    faculty_id,
    preloaded_schedule=None
):

    if preloaded_schedule is None:
        preloaded_schedule = {}

    # ---------------------------------
    # Clear toggle
    # ---------------------------------

    clear_key = "clear_schedule"

    if clear_key not in st.session_state:
        st.session_state[clear_key] = False

    use_preload = (
        bool(preloaded_schedule)
        and not st.session_state[clear_key]
    )

    # ---------------------------------
    # Config
    # ---------------------------------

    slot_timings = [
        "9:00 – 10:00", "10:00 – 11:00", "11:00 – 12:00", "12:00 – 1:00",
        "1:00 – 2:00", "2:00 – 3:00", "3:00 – 4:00", "4:00 – 5:00"
    ]

    departments = ["CSE", "AI&ML", "Cyber Security", "BCA"]
    years = ["1st", "2nd", "3rd", "4th"]
    task_options = ["Teaching", "Office Work", "Research", "Meeting", "Free", "Other"]

    # ---------------------------------
    # Preload banner
    # ---------------------------------

    prev_date = date.today() - timedelta(days=7)
    prev_day = prev_date.strftime("%A")
    prev_str = prev_date.strftime("%d %b %Y")

    if use_preload:
        st.info(
            f" Preloaded from **{prev_day}, {prev_str}** — review and edit before saving."
        )
        if st.button("✕ Start Fresh", use_container_width=True):
            st.session_state[clear_key] = True
            st.rerun()

    elif st.session_state[clear_key] and preloaded_schedule:
        st.warning("Showing blank schedule. Data from last week is available.")
        if st.button("↩ Restore Last Week", use_container_width=True):
            st.session_state[clear_key] = False
            st.rerun()

    # ---------------------------------
    # State Backup (Prevents data loss 
    # when toggling Teaching/Free)
    # ---------------------------------

    for i in range(8):
        for field in ["dep", "year", "topic", "remarks"]:
            key = f"{field}_{i}"
            if key in st.session_state:
                st.session_state[f"_bk_{key}"] = st.session_state[key]

    # ---------------------------------
    # Form UI
    # ---------------------------------

    st.subheader("Today's Schedule")

    activity_data = []

    for index, timing in enumerate(slot_timings):
        
        slot_number = index + 1
        slot_data = preloaded_schedule.get(slot_number, {}) if use_preload else {}

        st.markdown("---")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.subheader(timing)
            
            raw_task = slot_data.get("task_type", "Free")
            task_index = task_options.index(raw_task) if raw_task in task_options else task_options.index("Free")
            
            task_type = st.selectbox(
                "Task Type",
                task_options,
                index=task_index,
                key=f"task_{index}",
                label_visibility="collapsed"
            )

        # ---- Teaching fields ----
        if task_type == "Teaching":
            
            with col2:
                inner_col1, inner_col2 = st.columns(2)
                
                with inner_col1:
                    raw_dept = slot_data.get("department", "CSE")
                    default_dept = st.session_state.get(f"_bk_dep_{index}", raw_dept)
                    if default_dept not in departments:
                        default_dept = "CSE"
                        
                    st.radio(
                        "Department",
                        departments,
                        index=departments.index(default_dept),
                        horizontal=True,
                        key=f"dep_{index}"
                    )

                with inner_col2:
                    raw_year = slot_data.get("academic_year", "1st")
                    default_year = st.session_state.get(f"_bk_year_{index}", raw_year)
                    if default_year not in years:
                        default_year = "1st"
                        
                    st.radio(
                        "Year",
                        years,
                        index=years.index(default_year),
                        horizontal=True,
                        key=f"year_{index}"
                    )

                default_topic = st.session_state.get(f"_bk_topic_{index}", slot_data.get("topic_description", ""))
                
                st.text_input(
                    "What will you teach?",
                    value=default_topic,
                    placeholder="Example: Encapsulation, DBMS Joins, Inheritance",
                    key=f"topic_{index}"
                )

                default_remarks = st.session_state.get(f"_bk_remarks_{index}", slot_data.get("remarks", ""))
                
                st.text_input(
                    "Remarks (Optional)",
                    value=default_remarks,
                    key=f"remarks_{index}"
                )

        else:
            # For non-teaching, just an optional remarks field
            with col2:
                default_remarks = st.session_state.get(f"_bk_remarks_{index}", slot_data.get("remarks", ""))
                st.text_input(
                    "Remarks (Optional)",
                    value=default_remarks,
                    key=f"remarks_{index}"
                )

        # ---- Build Payload ----
        department = None
        academic_year = None
        topic = ""
        remarks = ""

        if task_type == "Teaching":
            department = st.session_state.get(f"dep_{index}")
            academic_year = st.session_state.get(f"year_{index}")
            topic = st.session_state.get(f"topic_{index}", "")
            
        remarks = st.session_state.get(f"remarks_{index}", "")

        activity_data.append({
            "faculty_id": faculty_id,
            "slot_number": slot_number,
            "task_type": task_type,
            "department": department,
            "academic_year": academic_year,
            "topic_description": topic,
            "remarks": remarks
        })

    st.markdown("---")

    if st.button("Save All", type="primary", use_container_width=True):
        st.session_state.pending_schedule_data = activity_data
        st.session_state.show_save_dialog = True

    # Trigger dialog if flag is set
    if st.session_state.get("show_save_dialog"):
        _show_save_dialog()