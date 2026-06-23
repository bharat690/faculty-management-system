import bcrypt
import pandas as pd

from utils.helper import (
    normalize_department
)

from queries.faculty_queries import (
    add_faculty_user,
    bulk_add_faculty,
    get_all_faculty,
    update_faculty,
    delete_faculty,
    reset_faculty_password,
    get_user_password_hash,
    update_user_password
)

def change_password(
    user_id,
    current_password,
    new_password,
    confirm_password
):

    if (
        new_password
        != confirm_password
    ):

        return (
            False,
            "Passwords do not match"
        )

    if len(
        new_password
    ) < 8:

        return (
            False,
            "Password must be at least 8 characters"
        )

    stored_hash = (
        get_user_password_hash(
            user_id
        )
    )

    if not (
        bcrypt.checkpw(
            current_password.encode(),
            stored_hash.encode()
        )
    ):

        return (
            False,
            "Current password incorrect"
        )

    hashed_password = (
        bcrypt.hashpw(
            new_password.encode(),
            bcrypt.gensalt()
        ).decode()
    )

    success = (
        update_user_password(
            user_id,
            hashed_password
        )
    )

    if success:

        return (
            True,
            "Password updated successfully"
        )

    return (
        False,
        "Password update failed"
    )




def update_faculty_details(
    faculty_id,
    full_name,
    email,
    department,
    skills
):

    return update_faculty(
        faculty_id,
        full_name,
        email,
        department,
        skills
    )


def remove_faculty(
    faculty_id
):

    return delete_faculty(
        faculty_id
    )


def reset_password(
    faculty_id,
    department
):

    department = (
        department
        .upper()
        .replace("&", "")
        .replace(" ", "")
    )

    new_password = (
        f"{department}2026@"
    )

    hashed_password = (
        bcrypt.hashpw(
            new_password.encode(),
            bcrypt.gensalt()
        ).decode()
    )

    success = (
        reset_faculty_password(
            faculty_id,
            hashed_password
        )
    )

    return (
        success,
        new_password
    )

def fetch_all_faculty():

    return (
        get_all_faculty()
    )


def create_faculty(
    employee_id,
    full_name,
    email,
    password,
    department,
    skills
):
    department = (
    normalize_department(
        department
    )
)

    hashed_password = (
        bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()
    )

    return add_faculty_user(
        employee_id,
        full_name,
        email,
        hashed_password,
        department,
        skills
    )


def bulk_create_faculty(
    uploaded_file
):

    df = pd.read_csv(
        uploaded_file
    )

    faculty_rows = []

    credentials = []

    for _, row in df.iterrows():

        department = (
            normalize_department(
                row["department"]
            )
        )

        password_map = {
            "CSE": "CSE2026@",
            "AI & ML": "AIML2026@",
            "CSA": "CSA2026@"
        }

        password = (
            password_map[
                department
            ]
        )

        hashed_password = (
            bcrypt.hashpw(
                password.encode(),
                bcrypt.gensalt()
            ).decode()
        )

        faculty_rows.append(
            (
                row["employee_id"],
                row["full_name"],
                row["email"],
                hashed_password,
                row["department"],
                row.get(
                    "skills",
                    ""
                )
            )
        )

        credentials.append({
            "employee_id":
            row["employee_id"],

            "email":
            row["email"],

            "password":
            password
        })

    success = (
        bulk_add_faculty(
            faculty_rows
        )
    )

    credentials_df = (
        pd.DataFrame(
            credentials
        )
    )

    return (
        success,
        credentials_df
    )
