from database.db import (
    get_connection
)


def get_all_semesters():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT
                id,
                semester_name,
                start_date,
                end_date,
                is_active
            FROM semesters
            ORDER BY id DESC
        """)

        return cursor.fetchall()

    finally:

        cursor.close()
        conn.close()


def get_active_semester():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT
                semester_name
            FROM semesters
            WHERE is_active = TRUE
            LIMIT 1
        """)

        result = (
            cursor.fetchone()
        )

        return (
            result[0]
            if result
            else "No Active Semester"
        )

    finally:

        cursor.close()
        conn.close()


def set_active_semester(
    semester_id
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # remove current active
        cursor.execute("""
            UPDATE semesters
            SET is_active = FALSE
        """)

        # set new active
        cursor.execute("""
            UPDATE semesters
            SET is_active = TRUE
            WHERE id = %s
        """, (
            semester_id,
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

def get_active_semester_id():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT id
            FROM semesters
            WHERE is_active = TRUE
            LIMIT 1
        """)

        result = (
            cursor.fetchone()
        )

        return (
            result[0]
            if result
            else None
        )

    finally:

        cursor.close()
        conn.close()



def start_new_semester(
    semester_name
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # -------------------
        # Reset activity data
        # -------------------

        cursor.execute("""
            DELETE FROM attendance
        """)

        cursor.execute("""
            DELETE FROM
            daily_activity_logs
        """)

        # -------------------
        # deactivate old
        # -------------------

        cursor.execute("""
            UPDATE semesters
            SET is_active = FALSE
        """)

        # -------------------
        # create new semester
        # -------------------

        cursor.execute("""
            INSERT INTO semesters
            (
                semester_name,
                start_date,
                end_date,
                is_active
            )
            VALUES
            (
                %s,
                CURRENT_DATE,
                CURRENT_DATE
                + INTERVAL '6 months',
                TRUE
            )
        """, (
            semester_name,
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
