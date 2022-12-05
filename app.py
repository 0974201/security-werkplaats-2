from flask import Flask, render_template, g, request
import sqlite3
import os.path

app = Flask(__name__)


@app.route("/")
def index():
    data = get_db()
    return render_template("detail-page.html", all_data=data)


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect("databases/testcorrect_vragen.db")
        cursor = db.cursor()
        cursor.execute("SELECT*FROM vragen ")
        all_data = cursor.fetchall()
    return all_data


@app.route("/filter_null")
def filter_null():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect("databases/testcorrect_vragen.db")
        cursor = db.cursor()
        cursor.execute("SELECT*FROM vragen WHERE leerdoel IS NULL")
        all_data = cursor.fetchall()
    return all_data


if __name__ == "__main__":
    app.run(debug=True)
