import os.path
import sys

from flask import Flask, render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
#from flask_login import login_required, current_user

from lib.tablemodel import DatabaseModel
from lib.demodatabase import create_demo_database
from lib.manageuser import *

# This demo glues a random database and the Flask framework. If the database file does not exist,
# a simple demo dataset will be created.
LISTEN_ALL = "0.0.0.0"
FLASK_IP = LISTEN_ALL
FLASK_PORT = 81
FLASK_DEBUG = True

app = Flask(__name__)
# This command creates the "<application directory>/databases/testcorrect_vragen.db" path
DATABASE_FILE = os.path.join(app.root_path, 'databases', 'testcorrect_kopie.db')

# Check if the database file exists. If not, create a demo database
if not os.path.isfile(DATABASE_FILE):
    print(f"Could not find database {DATABASE_FILE}, creating a demo database.")
    create_demo_database(DATABASE_FILE)
dbm = DatabaseModel(DATABASE_FILE)
user = ManageUser(DATABASE_FILE)

# Main route that shows a list of tables in the database
# Note the "@app.route" decorator. This might be a new concept for you.
# It is a way to "decorate" a function with additional functionality. You
# can safely ignore this for now - or look into it as it is a really powerful
# concept in Python.
@app.route("/")
def index():
    tables = dbm.get_table_list()
    return render_template(
        "tables.html", table_list=tables, database_file=DATABASE_FILE
    )

#login scherm
@app.route("/login")
def login():
    return render_template("login.html", database_file=DATABASE_FILE)

@app.route("/base") #base template
def base():
    return render_template("base.html")

@app.route("/adduser") #test add user template
def adduser():
    return render_template("adduser.html")

@app.route("/adduser", methods = ['POST']) #code to add values from form to db
def adduser_post():
    if request.method == 'POST':
        gebruikersnaam = request.form.get('gebruikersnaam') #gets username from form
        # gets password from form and hashes it to store in db
        wachtwoord = generate_password_hash(request.form.get('wachtwoord'), method = 'pbkdf2:sha256', salt_length = 8)
        admin = request.form.get('admin')

        if admin == "on":
            admin = 1
        else:
            admin = 0

        user.add_new_user(gebruikersnaam, wachtwoord, admin)

        return redirect(url_for("add_user_success.html"))
    else:
        return render_template("adduser.html")

@app.route("/add_user_success") #should show up after successful post
def add_user_success():
    return render_template("add_user_success.html")

@app.route("/login_success") #should show up after successful post
def login_success():
    return render_template("login_success.html")

@app.route("/demologin") #test login template
def demologin():
    return render_template("demologin.html")

@app.route("/demologin", methods = ['POST']) #well we've atleast one admin user now, dus tijd om login shit te doen
def demologin_post():
    if request.method == 'POST':
        gebruikersnaam = request.form.get('gebruikersnaam')
        wachtwoord = request.form.get('wachtwoord')
        return render_template("login_success.html", gebruikersnaam = gebruikersnaam)
    else:
        return render_template("demologin.html")

@app.route("/login") #test login template
def login():
    return render_template("login.html")

@app.route("/login", methods = ['POST']) #well we've atleast one admin user now, dus tijd om login shit te doen
def login_post():
    if request.method == 'POST':
        gebruikersnaam = request.form.get('gebruikersnaam')
        wachtwoord = request.form.get('wachtwoord')
        derp = user.check_user(gebruikersnaam, wachtwoord)
        print(derp)
        if check_password_hash(derp, wachtwoord):
            return redirect(url_for("login_success"))
    else:
        return render_template("login.html")


# The table route displays the content of a table
@app.route("/table_details/<table_name>")
def table_content(table_name=None):
    if not table_name:
        return "Missing table name", 400  # HTTP 400 = Bad Request
    else:
        rows, column_names = dbm.get_table_content(table_name)
        return render_template(
            "table_details.html", rows=rows, columns=column_names, table_name=table_name
        )

@app.route("/admin") #copypasta from above but points specifically to the login_test table
def admin(table_name="login_test"):
    if not table_name:
        return "Missing table name", 400  # HTTP 400 = Bad Request
    else:
        rows, column_names = dbm.get_table_content(table_name)
        return render_template(
            "admin.html", rows=rows, columns=column_names, table_name=table_name
        )

@app.route("/account_details") #copypasta from above but points specifically to the login_test table
def account_details():
        return "account_details.html",


@app.route("/teapot") #test
def test():
    return render_template("test.html"), 418       

if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)
