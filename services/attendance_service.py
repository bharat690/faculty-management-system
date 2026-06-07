from queries.attendance_queries import (
    get_today_attendance,
    mark_attendance
)

from queries.semester_queries import (
    get_active_semester
)


def attendance_already_marked(
    faculty_id
):

    attendance = get_today_attendance(
        faculty_id
    )

    return attendance is not None


def submit_attendance(
    faculty_id,
    status
):

    semester = get_active_semester()

    if not semester:
        return False

    semester_id = semester[0]

    return mark_attendance(
        faculty_id,
        semester_id,
        status
    )