from queries.schedule_queries import (
    save_daily_activity,
    check_today_activity_exists
)

from queries.semester_queries import (
    get_active_semester
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

    semester = (
        get_active_semester()
    )

    if not semester:
        return False

    semester_id = semester[0]

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
                item["academic_unit_id"],
                item["subject_id"],
                item["remarks"]
            )
        )

    return save_daily_activity(
        formatted_data
    )