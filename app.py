from flask import Flask, render_template, g
import sqlite3
import os.path

app = Flask(__name__)


@app.route("/")
def index():
    data = get_db()
    return str(data)


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect("databases/testcorrect_vragen.db")
        cursor = db.cursor()
        cursor.execute("select*from vragen")

    return cursor.fetchall()


if __name__ == "__main__":
    app.run(debug=True)
