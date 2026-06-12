from database.db import (
    get_connection
)



def get_today_faculty_status():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT
                u.full_name,
                COALESCE(
                    a.status,
                    'unmarked'
                ) as status
            FROM users u

            LEFT JOIN attendance a
            ON (
                u.id =
                a.faculty_id
                AND
                a.attendance_date =
                CURRENT_DATE
            )

            WHERE u.role =
            'faculty'

            ORDER BY
            u.full_name
        """)

        return (
            cursor.fetchall()
        )

    finally:

        cursor.close()
        conn.close()

def get_today_attendance_stats():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # ----------------------
        # Total Faculty
        # ----------------------

        cursor.execute("""
            SELECT COUNT(*)
            FROM users
            WHERE role = 'faculty'
        """)

        total_faculty = (
            cursor.fetchone()[0]
        )

        # ----------------------
        # Attendance
        # ----------------------

        cursor.execute("""
            SELECT
                status,
                COUNT(*)
            FROM attendance
            WHERE attendance_date =
            CURRENT_DATE
            GROUP BY status
        """)

        attendance_data = (
            cursor.fetchall()
        )

        stats = {
            "present": 0,
            "absent": 0,
            "unmarked": 0
        }

        for status, count in (
            attendance_data
        ):

            stats[status] = count

        stats["unmarked"] = (
            total_faculty
            - stats["present"]
            - stats["absent"]
        )

        return stats

    finally:

        cursor.close()
        conn.close()
        
def get_faculty_availability(
    slot_number
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT
                u.full_name,
                d.task_type,
                d.department,
                d.academic_year,
                d.topic_description
            FROM daily_activity_logs d
            JOIN users u
            ON d.faculty_id = u.id
            WHERE d.activity_date =
            CURRENT_DATE
            AND d.slot_number = %s
            ORDER BY u.full_name
        """, (slot_number,))

        return cursor.fetchall()

    finally:

        cursor.close()
        conn.close()