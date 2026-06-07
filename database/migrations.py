from .db import get_connection


def run_schema():

    conn = get_connection()

    if not conn:
        print("Database connection failed")
        return

    cursor = conn.cursor()

    try:
        with open("database/schema.sql", "r") as file:
            schema_sql = file.read()

        cursor.execute(schema_sql)

        conn.commit()

        print("Schema created successfully!")

    except Exception as e:
        conn.rollback()
        print("Migration failed:", e)

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    run_schema()