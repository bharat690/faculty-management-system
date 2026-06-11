from queries.semester_queries import (
    get_all_semesters,
    get_active_semester,
    set_active_semester,
    start_new_semester
)


def fetch_semesters():

    return (
        get_all_semesters()
    )


def fetch_active_semester():

    return (
        get_active_semester()
    )


def change_semester(
    semester_id
):

    return (
        set_active_semester(
            semester_id
        )
    )


def initialize_new_semester(
    semester_name
):

    return (
        start_new_semester(
            semester_name
        )
    )


