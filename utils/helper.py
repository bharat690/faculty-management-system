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

        # CSE
        "cse": "CSE",
        "computer science": "CSE",
        "b.tech cse": "CSE",
        "m.tech cse": "CSE",

        # AI & ML
        "ai & ml": "AI & ML",
        "ai&ml": "AI & ML",
        "ai &ml": "AI & ML",
        "ai& ml": "AI & ML",
        "artificial intelligence": "AI & ML",
        "aiml": "AI & ML",
        "b.tech aiml": "AI & ML",
        "b.tech ai&ml": "AI & ML",
        "b.tech cyber security": "AI & ML",
        "cyber security": "AI & ML",
        "cybersecurity": "AI & ML",
        "cyber": "AI & ML",
        "b.tech data science": "AI & ML",
        "data science": "AI & ML",

        # CSA
        "csa": "CSA",
        "bca": "CSA",
        "mca": "CSA",
        "computer science application": "CSA"
    }

    return (
        department_mapping.get(
            department,
            "CSE"
        )
    )