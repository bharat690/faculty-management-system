
from database.db import (
    get_connection
)


def get_faculty_list():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT
                id,
                employee_id,
                full_name,
                department
            FROM users
            WHERE role =
            'faculty'
            ORDER BY full_name
        """)

        return (
            cursor.fetchall()
        )

    finally:

        cursor.close()
        conn.close()
        
def get_faculty_summary(
    faculty_id,
    start_date,
    end_date
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT
                COUNT(
                    CASE
                    WHEN status =
                    'present'
                    THEN 1
                    END
                ) as present_days
            FROM attendance
            WHERE faculty_id =
            %s
            AND attendance_date
            BETWEEN %s
            AND %s
        """, (
            faculty_id,
            start_date,
            end_date
        ))

        attendance = (
            cursor.fetchone()[0]
        )

        cursor.execute("""
            SELECT
                COUNT(
                    CASE
                    WHEN task_type =
                    'Teaching'
                    THEN 1
                    END
                ) as teaching_hours,

                COUNT(
                    CASE
                    WHEN task_type IN (
                        'Office Work',
                        'Meeting',
                        'Research',
                        'Exam Duty'
                    )
                    THEN 1
                    END
                ) as work_hours,

                COUNT(
                    CASE
                    WHEN task_type =
                    'Free'
                    THEN 1
                    END
                ) as free_hours

            FROM daily_activity_logs
            WHERE faculty_id =
            %s
            AND activity_date
            BETWEEN %s
            AND %s
        """, (
            faculty_id,
            start_date,
            end_date
        ))

        activity = (
            cursor.fetchone()
        )

        return {

            "present_days":
            attendance or 0,

            "teaching_hours":
            activity[0] or 0,

            "work_hours":
            activity[1] or 0,

            "free_hours":
            activity[2] or 0
        }

    finally:

        cursor.close()
        conn.close()

def get_weekly_classes(
    faculty_id
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT
                activity_date,
                slot_number,
                department,
                academic_year,
                topic_description

            FROM daily_activity_logs

            WHERE faculty_id =
            %s

            AND task_type =
            'Teaching'

            AND activity_date >=
            CURRENT_DATE - INTERVAL
            '7 days'

            ORDER BY
            activity_date,
            slot_number
        """, (
            faculty_id,
        ))

        return (
            cursor.fetchall()
        )

    finally:

        cursor.close()
        conn.close()


def get_topics_by_class(
    faculty_id
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT
                department,
                academic_year,
                topic_description

            FROM daily_activity_logs

            WHERE faculty_id =
            %s

            AND task_type =
            'Teaching'

            AND topic_description
            IS NOT NULL

            ORDER BY
            department,
            academic_year
        """, (
            faculty_id,
        ))

        return (
            cursor.fetchall()
        )

    finally:

        cursor.close()
        conn.close()
