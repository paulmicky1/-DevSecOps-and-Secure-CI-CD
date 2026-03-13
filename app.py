import sqlite3

from flask import Flask, jsonify, request


app = Flask(__name__)
DB_PATH = "app.db"


def init_db() -> None:
    """Create a simple local SQLite database for demo usage."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


@app.route("/", methods=["GET"])
def index():
    return jsonify(
        {
            "message": "DevSecOps demo API is running.",
            "usage": "/search?q=<term>",
        }
    )


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    sql = "SELECT id, name FROM items WHERE name LIKE ?"
    cursor.execute(sql, (f"%{query}%",))
    rows = cursor.fetchall()
    conn.close()

    return jsonify([{"id": row[0], "name": row[1]} for row in rows])


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
# Triggering a new pipeline run
