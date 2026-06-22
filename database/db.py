import os
import psycopg2
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def get_database_url():

    # Streamlit Cloud
    if "DATABASE_URL" in st.secrets:
        return st.secrets[
            "DATABASE_URL"
        ]

    # Local .env
    return os.getenv(
        "DATABASE_URL"
    )


def get_connection():

    try:

        conn = psycopg2.connect(
            get_database_url(),
            sslmode="require"
        )

        return conn

    except Exception as e:

        print(
            "Database connection failed:",
            e
        )

        return None