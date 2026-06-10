from database.db import get_connection


def save_daily_activity(
    activity_data
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        query = """
        INSERT INTO daily_activity_logs
        (
            faculty_id,
            semester_id,
            activity_date,
            slot_number,
            start_time,
            end_time,
            task_type,
            department,
            academic_year,
            topic_description,
            remarks
        )
        VALUES
        (
            %s, %s,
            CURRENT_DATE,
            %s, %s, %s,
            %s, %s, %s,
            %s, %s
        )

        ON CONFLICT
        (
            faculty_id,
            activity_date,
            slot_number
        )

        DO UPDATE SET

        task_type =
        EXCLUDED.task_type,

        department =
        EXCLUDED.department,

        academic_year =
        EXCLUDED.academic_year,

        topic_description =
        EXCLUDED.topic_description,

        remarks =
        EXCLUDED.remarks
        """

        cursor.executemany(
            query,
            activity_data
        )

        conn.commit()

        return True

    except Exception as e:

        conn.rollback()

        print(e)

        return False

    finally:

        cursor.close()
        conn.close()

def check_today_activity_exists(
    faculty_id
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT id
            FROM daily_activity_logs
            WHERE faculty_id = %s
            AND activity_date =
            CURRENT_DATE
            LIMIT 1
        """, (faculty_id,))

        return cursor.fetchone()

    except Exception as e:

        print(e)
        return None

    finally:

        cursor.close()
        conn.close()