from database.db import get_connection


def get_active_semester():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT id,
                   semester_name
            FROM semesters
            WHERE is_active = TRUE
            LIMIT 1
        """)

        return cursor.fetchone()

    except Exception as e:
        print(e)
        return None

    finally:
        cursor.close()
        conn.close()