from queries.faculty_queries import (
    get_user_by_email
)

from utils.password_hash import (
    verify_password
)


def login_user(email, password):

    user = get_user_by_email(email)

    if not user:
        return None

    (
        user_id,
        full_name,
        user_email,
        password_hash,
        role,
        department
    ) = user

    is_valid = verify_password(
        password,
        password_hash
    )

    if not is_valid:
        return None

    return {
        "id": user_id,
        "name": full_name,
        "email": user_email,
        "role": role,
        "department": department
    }