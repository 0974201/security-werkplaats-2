from flask import Flask, render_template
import sqlite3
import os.path

app = Flask(__name__)


@app.route("/")
def index():
    data = get_db()
    return render_template("detail-page.html", all_data=data)


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "vragen")
with sqlite3.connect(db_path) as db:
    db


def get_db():
    db = getattr(app, "db", None)
    if db is None:
        db = sqlite3.connect("testcorrect_vragen.db")
        cursor = db.cursor()
        cursor.execute("select * from vragen")
    return cursor.fetchall()


if __name__ == "__main__":
    app.run(debug=True)
