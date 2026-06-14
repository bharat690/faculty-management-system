from datetime import datetime
from zoneinfo import (
    ZoneInfo
)


def get_current_slot():

    current_hour = (
        datetime.now(
            ZoneInfo(
                "Asia/Kolkata"
            )
        ).hour
    )

    slot_map = {
        9: 1,
        10: 2,
        11: 3,
        12: 4,
        13: 5,
        14: 6,
        15: 7,
        16: 8
    }

    return slot_map.get(
        current_hour,
        None
    )

def normalize_department(
    department
):

    department = (
        str(department)
        .strip()
        .lower()
    )

    department_mapping = {

        "cse":
        "CSE",

        "computer science":
        "CSE",

        "aiml":
        "AI&ML",

        "ai&ml":
        "AI&ML",

        "ai & ml":
        "AI&ML",

        "artificial intelligence":
        "AI&ML",

        "cyber security":
        "Cyber Security",

        "cybersecurity":
        "Cyber Security",

        "cyber":
        "Cyber Security",

        "bca":
        "BCA"
    }

    return (
        department_mapping.get(
            department,
            "CSE"
        )
    )