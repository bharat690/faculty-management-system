from queries.analytics_queries import (
    get_today_attendance_stats,
    get_faculty_availability
)


def fetch_dashboard_stats():

    return (
        get_today_attendance_stats()
    )


def fetch_faculty_availability(
    slot_number
):

    return (
        get_faculty_availability(
            slot_number
        )
    )