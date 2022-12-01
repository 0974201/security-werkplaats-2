from flask import Flask, render_template, g, request
import sqlite3
import os.path

app = Flask(__name__)


@app.route("/")
def index():
    data = get_db()
    return render_template("detail-page.html", all_data=data)


@app.route("/add_items", methods=["post"])
def add_items():
    return request.form["select_items "]


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect("databases/testcorrect_vragen.db")
        cursor = db.cursor()
        cursor.execute("SELECT vraag FROM vragen")
        all_data = cursor.fetchall()
    return all_data


if __name__ == "__main__":
    app.run(debug=True)
