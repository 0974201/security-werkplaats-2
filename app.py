import os.path
import sys

from flask import Flask, render_template, redirect, url_for, session, request, flash, send_from_directory
#from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user

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

app.config['SECRET_KEY'] = 'nee'
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

@app.before_request
def check_login():
    if request.endpoint not in ["login", "login_post"]:
        if not session.get('logged_in'):
            return redirect(url_for('login'))

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/index")
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    tables = dbm.get_table_list()
    return render_template(
        "tables.html", table_list=tables, database_file=DATABASE_FILE
    )

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

@app.route("/base") #base template
def base():
    return render_template("base.html")

@app.route("/adduser") #test add user template
def adduser():
    return render_template("adduser.html")

@app.route("/adduser", methods = ['POST']) #code to add values from form to db
def adduser_post():
    if request.method == 'POST':
        gebruikersnaam = request.form.get('gebruikersnaam').strip() #gets username from form
        wachtwoord = request.form.get('wachtwoord')
        # gets password from form and hashes it to store in db
        #wachtwoord = generate_password_hash(request.form.get('wachtwoord'), method = 'pbkdf2:sha256', salt_length = 8)
        admin = request.form.get('admin')

        if admin == "on":
            admin = 1
        else:
            admin = 0

        user.add_new_user(gebruikersnaam, wachtwoord, admin)

        flash("user created", 'info') #shows after successfull user creattoion
        return render_template("adduser.html")
    else:
        flash("u done goofed", 'warning')
        return render_template("adduser.html")


@app.route("/login_success") #should show up after successful post
#@login_required
def login_success():
    return render_template("login_success.html")
    
@app.route("/login") #test login template
def login():
    return render_template("login.html")

@app.route("/login", methods = ['POST']) # login post, it works for now i guess??
def login_post():
    if request.method == 'POST':
        gebruikersnaam = request.form.get('gebruikersnaam')
        wachtwoord = request.form.get('wachtwoord')
        check_user = user.login_user(gebruikersnaam, wachtwoord) #checks if user is in db, returns none if not present
        if check_user:
            session["logged_in"] = True
            session["username"] = gebruikersnaam
            print(session["logged_in"])
            print(session["username"])
            return redirect(url_for("index"))
        elif check_user == None:
            flash("u done goofed", 'warning')
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route("/logout") #test login template
def logout():
    session["logged_in"] = False
    session.pop("username")
    print(session["logged_in"])
    return redirect(url_for('index'))

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
        rows, column_names = dbm.get_admin_table_content(table_name)
        return render_template(
            "admin.html", rows=rows, columns=column_names, table_name=table_name
        )

@app.route("/account_details/<id>") #gets id to load user from db
def account_details(id):
        user_info = user.get_user(id)
        #print(user_info)

        id = user_info[0]
        gebruikersnaam = user_info[1]
        wachtwoord = user_info[2]
        admin = user_info[3]

        #print(f"{id}, {gebruikersnaam}, {wachtwoord}, {admin}")

        return render_template("account_details.html",id = id, gebruikersnaam = gebruikersnaam, wachtwoord = wachtwoord, admin = admin)

@app.route("/editaccount/<id>", methods = ['GET', 'POST']) #gets id to load user from db
def edit_account_post(id):
    if request.method == 'POST':
        
        gebruikersnaam = request.form.get('gebruikersnaam').strip()
        wachtwoord = request.form.get('wachtwoord')
        admin = request.form.get('admin')

        if admin == "on":
            admin = 1
        else:
            admin = 0

        user.edit_user(gebruikersnaam, wachtwoord, admin, id)

        flash("edited user", 'info')
        return render_template("admin.html") 
    else:
        flash("u done goofed", 'warning')
        return render_template("admin.html")   

@app.route("/delete_account/<id>") #gets id to load user from db
def delete_account(id):
        user.delete_user(id)

        flash("yeet", 'warning')
        return render_template("admin.html")        


@app.route("/teapot") #test
def test():
    return render_template("test.html"), 418       

if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)
