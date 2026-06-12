from queries.attendance_queries import (
    get_today_attendance,
    mark_attendance
)

from queries.semester_queries import (
    get_active_semester_id,

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

    semester_id = (
        get_active_semester_id()
    )

    if not semester_id:
        return False

    return mark_attendance(
        faculty_id,
        semester_id,
        status
    )
