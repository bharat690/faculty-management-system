from database.db import get_connection


def get_user_by_email(email):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT
                id,
                full_name,
                email,
                password_hash,
                role,
                department
            FROM users
            WHERE email = %s
        """, (email,))

        user = cursor.fetchone()

        return user

    except Exception as e:
        print("Query error:", e)
        return None

    finally:
        cursor.close()
        conn.close()