import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    try:
        conn = psycopg2.connect(
            os.getenv("DATABASE_URL")
        )
        return conn

    except Exception as e:
        print("Database connection failed:", e)
        return None