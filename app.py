import os.path
import sys

import io
import csv

from flask import Flask, render_template, make_response, request

from flask import Flask, render_template, redirect, url_for, request


from lib.tablemodel import DatabaseModel
from lib.demodatabase import create_demo_database

# This demo glues a random database and the Flask framework. If the database file does not exist,
# a simple demo dataset will be created.
LISTEN_ALL = "0.0.0.0"
FLASK_IP = LISTEN_ALL
FLASK_PORT = 81
FLASK_DEBUG = True

app = Flask(__name__)
# This command creates the "<application directory>/databases/testcorrect_vragen.db" path
DATABASE_FILE = os.path.join(app.root_path, "databases", "testcorrect_vragen.db")
DATABASE_FILE = os.path.join(app.root_path, "databases", "testcorrect_vragen.db")

# Check if the database file exists. If not, create a demo database
if not os.path.isfile(DATABASE_FILE):
    print(f"Could not find database {DATABASE_FILE}, creating a demo database.")
    create_demo_database(DATABASE_FILE)
dbm = DatabaseModel(DATABASE_FILE)

# Main route that shows a list of tables in the database
# Note the "@app.route" decorator. This might be a new concept for you.
# It is a way to "decorate" a function with additional functionality. You
# can safely ignore this for now - or look into it as it is a really powerful
# concept in Python.


@app.route("/")
def tables():
    tables = dbm.get_table_list()
    return render_template(
        "tables.html", table_list=tables, database_file=DATABASE_FILE
    )


@app.route("/home")
def index():
    return render_template("index.html")


# The table route displays the content of a table
@app.route("/table_details/<table_name>")
def table_content(table_name=None):
    if not table_name:
        return "Missing table name", 400  # HTTP 400 = Bad Request
    else:
        rows, column_names = dbm.get_table_content(table_name)
        return render_template(
            "table_details.html",
            rows=rows,
            columns=column_names,
            table_name=table_name,
        )


# Invalid leerdoel route
@app.route("/invalid_leerdoel/<table_name>")
def invalid_leerdoel(table_name=None):
    if not table_name:
        return "Missing table name", 400
    else:
        rows, column_names = dbm.check_invalid(
            table_name, "leerdoel", "id", "leerdoelen"
        )
        return render_template(
            "invalid_leerdoel.html",
            rows=rows,
            columns=column_names,
            table_name=table_name,
        )


# Html codes in vragen
@app.route("/html_codes/<table_name>")
def html_codes(table_name=None):
    if not table_name:
        return "Missing table name", 400
    else:
        rows, column_names = dbm.get_html_codes(table_name, "vraag")
        return render_template(
            "html_codes.html",
            rows=rows,
            columns=column_names,
            table_name=table_name,
        )


# Full table
@app.route("/csv_export_full/<table_name>")
def csv_export_full(table_name=None):
    if not table_name:
        return "Missing table name", 400
    else:
        rows, column_names = dbm.get_table_content(table_name)
        si = io.StringIO()
        cw = csv.writer(si)
        cw.writerow(column_names)
        cw.writerows(rows)
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
        return output


# Invalid leerdoel
@app.route("/csv_export_invalid/<table_name>")
def csv_export_invalid(table_name=None):
    if not table_name:
        return "Missing table name", 400
    else:
        rows, column_names = dbm.check_invalid(
            table_name, "leerdoel", "id", "leerdoelen"
        )
        si = io.StringIO()
        cw = csv.writer(si)
        cw.writerow(column_names)
        cw.writerows(rows)
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
        return output


# Html codes in vragen
@app.route("/csv_export_html/<table_name>")
def csv_export_html(table_name=None):
    if not table_name:
        return "Missing table name", 400
    else:
        rows, column_names = dbm.get_html_codes(table_name, "vraag")
        si = io.StringIO()
        cw = csv.writer(si)
        cw.writerow(column_names)
        cw.writerows(rows)
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
        return output


@app.route("/max_value/<table_name>", methods=["POST"])
def min_max(table_name=None):
    if not table_name:
        return "Missing table name", 400
    else:
        num1 = request.form["min"]
        num2 = request.form["max"]
        rows, column_names = dbm.get_min_max(table_name, num1, num2)
        return render_template(
            "table_details.html",
            rows=rows,
            columns=column_names,
            table_name=table_name,
            num1=num1,
            num2=num2,
        )



# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)





if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)
