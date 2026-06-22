from queries.schedule_queries import (
    save_daily_activity,
    check_today_activity_exists,
    get_previous_week_day_schedule,

)
from queries.semester_queries import (
    get_active_semester_id
)


def activity_already_submitted(
    faculty_id
):

    activity = (
        check_today_activity_exists(
            faculty_id
        )
    )

    return activity is not None


def submit_daily_schedule(
    activity_data
):

    semester_id = (
        get_active_semester_id()
    )

    if not semester_id:
        return False

    formatted_data = []

    timings = [
        ("09:00", "10:00"),
        ("10:00", "11:00"),
        ("11:00", "12:00"),
        ("12:00", "01:00"),
        ("01:00", "02:00"),
        ("02:00", "03:00"),
        ("03:00", "04:00"),
        ("04:00", "05:00")
    ]

    for index, item in enumerate(
        activity_data
    ):

        start_time, end_time = (
            timings[index]
        )

        formatted_data.append(
    (
        item["faculty_id"],
        semester_id,
        item["slot_number"],
        start_time,
        end_time,
        item["task_type"],
        item["department"],
        item["academic_year"],
        item["topic_description"],
        item["remarks"]
    )
)

    return save_daily_activity(
        formatted_data
    )


def fetch_previous_week_template(faculty_id):

    rows = get_previous_week_day_schedule(faculty_id)

    template = {}

    for row in rows:

        (
            slot_number,
            task_type,
            department,
            academic_year,
            topic,
            remarks
        ) = row

        template[slot_number] = {
            "task_type": task_type,
            "department": department,
            "academic_year": academic_year,
            "topic_description": topic,
            "remarks": remarks
        }

    return template