from faker import Faker
import bcrypt

from .db import get_connection


fake = Faker()


def hash_password(password):
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def seed_database():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # ----------------------------
        # Departments
        # ----------------------------

        departments = [
            ("Artificial Intelligence & ML", "AIML"),
            ("Computer Science Engineering", "CSE"),
            ("Electronics Engineering", "ECE"),
            ("Mechanical Engineering", "ME"),
            ("Civil Engineering", "CE")
        ]

        cursor.executemany(
            """
            INSERT INTO departments
            (department_name, department_code)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
            """,
            departments
        )

        # ----------------------------
        # Semester
        # ----------------------------

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
                'Jan-Jun 2026',
                '2026-01-01',
                '2026-06-30',
                TRUE
            )
            ON CONFLICT DO NOTHING
        """)

        # ----------------------------
        # Academic Units
        # ----------------------------

        cursor.execute("""
            SELECT id
            FROM departments
        """)

        departments_db = cursor.fetchall()

        academic_units = []

        for dept in departments_db:
            dept_id = dept[0]

            for year in range(1, 5):

                for section in ['A', 'B']:

                    academic_units.append(
                        (
                            dept_id,
                            year,
                            section
                        )
                    )

        cursor.executemany(
            """
            INSERT INTO academic_units
            (
                department_id,
                year,
                section
            )
            VALUES (%s, %s, %s)
            """,
            academic_units
        )

        # ----------------------------
        # Subjects
        # ----------------------------

        sample_subjects = [
            ("DBMS", "CS101"),
            ("Operating Systems", "CS102"),
            ("Computer Networks", "CS103"),
            ("Machine Learning", "AI201"),
            ("Deep Learning", "AI202"),
            ("Data Structures", "CS104"),
            ("Mathematics", "MA101")
        ]

        for dept in departments_db:

            dept_id = dept[0]

            for subject_name, subject_code in sample_subjects:

                try:
                    cursor.execute("""
                        INSERT INTO subjects
                        (
                            subject_name,
                            subject_code,
                            department_id,
                            year
                        )
                        VALUES (%s, %s, %s, %s)
                    """, (
                        subject_name,
                        f"{subject_code}_{dept_id}",
                        dept_id,
                        fake.random_int(
                            min=1,
                            max=4
                        )
                    ))

                except:
                    pass

        # ----------------------------
        # Dean User
        # ----------------------------

        dean_password = hash_password("admin123")

        cursor.execute("""
            INSERT INTO users
            (
                employee_id,
                full_name,
                email,
                password_hash,
                role,
                department
            )
            VALUES
            (
                'DEAN001',
                'Dean User',
                'dean@college.edu',
                %s,
                'dean',
                'Administration'
            )
            ON CONFLICT (email)
            DO NOTHING
        """, (dean_password, ))

        # ----------------------------
        # Faculty Users
        # ----------------------------

        department_names = [
            "AIML",
            "CSE",
            "ECE",
            "ME",
            "CE"
        ]

        faculty_users = []

        for i in range(1, 11):

            faculty_users.append(
                (
                    f"FAC{i:03}",
                    fake.name(),
                    f"faculty{i}@college.edu",
                    hash_password("faculty123"),
                    "faculty",
                    fake.random_element(
                        department_names
                    ),
                    fake.job()
                )
            )

        cursor.executemany("""
            INSERT INTO users
            (
                employee_id,
                full_name,
                email,
                password_hash,
                role,
                department,
                skills
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (email)
            DO NOTHING
        """, faculty_users)

        conn.commit()

        print("Database seeded successfully!")

    except Exception as e:
        conn.rollback()
        print("Seeding failed:", e)

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    seed_database()