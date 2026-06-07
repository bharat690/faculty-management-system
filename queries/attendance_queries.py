from database.db import get_connection


def get_today_attendance(
    faculty_id
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT status
            FROM attendance
            WHERE faculty_id = %s
            AND attendance_date = CURRENT_DATE
        """, (faculty_id,))

        return cursor.fetchone()

    except Exception as e:
        print(e)
        return None

    finally:
        cursor.close()
        conn.close()


def mark_attendance(
    faculty_id,
    semester_id,
    status
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO attendance
            (
                faculty_id,
                semester_id,
                attendance_date,
                status
            )
            VALUES
            (
                %s,
                %s,
                CURRENT_DATE,
                %s
            )
        """, (
            faculty_id,
            semester_id,
            status
        ))

        conn.commit()

        return True

    except Exception as e:
        conn.rollback()
        print(e)
        return False

    finally:
        cursor.close()
        conn.close()