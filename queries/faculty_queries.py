from database.db import get_connection
import streamlit as st

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

@st.cache_data
def get_departments():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id,
               department_name
        FROM departments
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data

@st.cache_data
def get_subjects():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id,
               subject_name
        FROM subjects
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data

@st.cache_data
def get_academic_units():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            year,
            section
        FROM academic_units
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data

def add_faculty_user(
    employee_id,
    full_name,
    email,
    password_hash,
    department,
    skills
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
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
            VALUES
            (
                %s, %s, %s,
                %s,
                'faculty',
                %s,
                %s
            )
        """, (
            employee_id,
            full_name,
            email,
            password_hash,
            department,
            skills
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
        
def bulk_add_faculty(
    faculty_data
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

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
            VALUES
            (
                %s, %s, %s,
                %s,
                'faculty',
                %s,
                %s
            )
        """, faculty_data)

        conn.commit()

        return True

    except Exception as e:

        conn.rollback()

        print(e)

        return False

    finally:

        cursor.close()
        conn.close()
        

def get_all_faculty():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT
                id,
                employee_id,
                full_name,
                email,
                department,
                skills
            FROM users
            WHERE role = 'faculty'
            ORDER BY full_name
        """)

        return cursor.fetchall()

    finally:

        cursor.close()
        conn.close()
        
        
def update_faculty(
    faculty_id,
    full_name,
    email,
    department,
    skills
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            UPDATE users
            SET
                full_name = %s,
                email = %s,
                department = %s,
                skills = %s
            WHERE id = %s
        """, (
            full_name,
            email,
            department,
            skills,
            faculty_id
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


def delete_faculty(
    faculty_id
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            DELETE FROM users
            WHERE id = %s
        """, (faculty_id,))

        conn.commit()

        return True

    except Exception as e:

        conn.rollback()

        print(e)

        return False

    finally:

        cursor.close()
        conn.close()


def reset_faculty_password(
    faculty_id,
    hashed_password
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            UPDATE users
            SET password_hash = %s
            WHERE id = %s
        """, (
            hashed_password,
            faculty_id
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