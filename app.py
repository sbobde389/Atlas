import os
import sqlite3

from flask import Flask, jsonify, render_template, request

app = Flask(__name__, template_folder="template")
DATABASE = "services.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search")
def search():
    query = (request.args.get("q") or "").strip()
    if not query:
        return jsonify({"error": "Please enter a service number."}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT service_no, latitude, longitude
        FROM services
        WHERE service_no = ?
           OR CAST(service_no AS TEXT) LIKE ?
        ORDER BY CASE WHEN service_no = ? THEN 0 ELSE 1 END, service_no
        LIMIT 10
        """,
        (query, f"{query}%", query),
    )
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return jsonify(rows)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug, host="0.0.0.0", port=port)
