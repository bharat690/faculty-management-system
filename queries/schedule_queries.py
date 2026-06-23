from database.db import get_connection
def get_schedule_for_date(faculty_id, target_date):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT
                slot_number,
                task_type,
                department,
                academic_year,
                topic_description,
                remarks
            FROM daily_activity_logs
            WHERE faculty_id = %s
            AND activity_date = %s
            ORDER BY slot_number
        """, (faculty_id, target_date))

        return cursor.fetchall()

    finally:

        cursor.close()
        conn.close()


def get_most_recent_activity_date(faculty_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT activity_date 
            FROM daily_activity_logs 
            WHERE faculty_id = %s 
            AND activity_date < CURRENT_DATE
            ORDER BY activity_date DESC 
            LIMIT 1
        """, (faculty_id,))

        result = cursor.fetchone()
        return result[0] if result else None

    finally:

        cursor.close()
        conn.close()

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
        
def get_previous_week_day_schedule(faculty_id, target_date):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT
                slot_number,
                task_type,
                department,
                academic_year,
                topic_description,
                remarks
            FROM daily_activity_logs
            WHERE faculty_id = %s
            AND activity_date = %s
            ORDER BY slot_number
        """, (faculty_id, target_date))

        return cursor.fetchall()

    finally:

        cursor.close()
        conn.close()