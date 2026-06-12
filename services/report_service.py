from datetime import (
    date,
    timedelta
)

from queries.report_queries import (
    get_faculty_list,
    get_faculty_summary,
    get_weekly_classes,
    get_topics_by_class
)

from queries.semester_queries import (
    get_active_semester_details
)


def fetch_faculty_list():

    return (
        get_faculty_list()
    )


def fetch_week_summary(
    faculty_id
):

    end_date = (
        date.today()
    )

    start_date = (
        end_date
        - timedelta(days=7)
    )

    return (
        get_faculty_summary(
            faculty_id,
            start_date,
            end_date
        )
    )


def fetch_month_summary(
    faculty_id
):

    end_date = (
        date.today()
    )

    start_date = (
        end_date
        - timedelta(days=30)
    )

    return (
        get_faculty_summary(
            faculty_id,
            start_date,
            end_date
        )
    )


def fetch_semester_summary(
    faculty_id
):

    semester = (
        get_active_semester_details()
    )

    if not semester:

        return {
            "present_days": 0,
            "teaching_hours": 0,
            "work_hours": 0,
            "free_hours": 0
        }

    start_date = semester[2]
    end_date = semester[3]

    return (
        get_faculty_summary(
            faculty_id,
            start_date,
            end_date
        )
    )


def fetch_weekly_classes(
    faculty_id
):

    return (
        get_weekly_classes(
            faculty_id
        )
    )


def fetch_topics_by_class(
    faculty_id
):

    return (
        get_topics_by_class(
            faculty_id
        )
    )
