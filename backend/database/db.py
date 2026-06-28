import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sop_database.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


def init_db():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        from database.schema import CREATE_SOPS_TABLE
        cursor.executescript(CREATE_SOPS_TABLE)
        conn.commit()
    finally:
        conn.close()
