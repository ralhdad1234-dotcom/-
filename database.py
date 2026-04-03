import sqlite3

conn = sqlite3.connect("db.db", check_same_thread=False)
c = conn.cursor()

def setup():
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        points INTEGER DEFAULT 0
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS deposits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL,
        tx TEXT,
        status TEXT
    )
    """)

    conn.commit()