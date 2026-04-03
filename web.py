from flask import Flask
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    conn = sqlite3.connect("db.db")
    c = conn.cursor()
    users = c.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    pts = c.execute("SELECT SUM(points) FROM users").fetchone()[0]
    return f"""
    <h1>VIP PANEL</h1>
    <p>Users: {users}</p>
    <p>Points: {pts}</p>
    """

app.run(port=5000)