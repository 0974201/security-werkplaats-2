import os.path
import sys

from flask import Flask, render_template, redirect, url_for, session, request, flash, send_from_directory
#from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash

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
#f_bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = 'nee'
# This command creates the "<application directory>/databases/testcorrect_vragen.db" path
DATABASE_FILE = os.path.join(app.root_path, 'databases', 'testcorrect_vragen.db')

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
        if not session.get('logged_in', 'username'):
            return redirect(url_for('login'))

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/index")
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    username = session.get('username')
    
    tables = dbm.get_table_list()
    return render_template(
        "tables.html", table_list=tables, database_file=DATABASE_FILE, username = username
    )

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

@app.route("/base") #base template
def base():
    return render_template("base.html")

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
            return redirect(url_for("login"))
    else:
        return render_template("login.html")

@app.route("/logout") #test login template
def logout():
    session["logged_in"] = False
    session.pop("username")
    print(session["logged_in"])
    return redirect(url_for('index'))

@app.route("/edit/<id>")
def edit(id):
    tbl_info = dbm.get_vraag_table_content
    print(tbl_info)

    #id = tbl_info[0]
    #vraag = tbl_info[1]
    #id=id, vraag=vraag
    return render_template("edit.html")

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
def admin(table_name="users"):
    if session.get('username') != "admin":
        return redirect(url_for('index'))

    if not table_name:
        return "Missing table name", 400  # HTTP 400 = Bad Request
    else:
        rows, column_names = dbm.get_admin_table_content(table_name)
        return render_template(
            "admin.html", rows=rows, columns=column_names, table_name=table_name
        )

@app.route("/adduser") #test add user template
def adduser():
    if session.get('username') != "admin":
        return redirect(url_for('index'))
    return render_template("adduser.html")

@app.route("/adduser", methods = ['POST']) #code to add values from form to db
def adduser_post():
    if request.method == 'POST':
        gebruikersnaam = request.form.get('gebruikersnaam').strip() #gets username from form
        wachtwoord = request.form.get('wachtwoord')
        #gets password from form and hashes it to store in db
        #wachtwoord = f_bcrypt.generate_password_hash(request.form.get('wachtwoord'))
        admin = request.form.get('admin')

        if admin == "on":
            admin = 1
        else:
            admin = 0

        user.add_new_user(gebruikersnaam, wachtwoord, admin)

        flash("user created", 'info') #shows after successfull user creattoion
        return redirect(url_for('admin'))
    else:
        flash("u done goofed", 'warning')
        return redirect(url_for('admin'))

@app.route("/account_details/<id>") #gets id to load user from db
def account_details(id):
    if session.get('username') != "admin":
        return redirect(url_for('index'))

    user_info = user.get_user(id)
    #print(user_info)

    id = user_info[0]
    gebruikersnaam = user_info[1]
    wachtwoord = user_info[2]
    admin = user_info[3]

    #print(f"{id}, {gebruikersnaam}, {wachtwoord}, {admin}")

    return render_template("account_details.html", id = id, gebruikersnaam = gebruikersnaam, wachtwoord = wachtwoord, admin = admin)

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
        return redirect(url_for('admin'))
    else:
        flash("u done goofed", 'warning')
        return redirect(url_for('admin'))   

@app.route("/delete_account/<id>") #gets id to load user from db
def delete_account(id):
    if session.get('username') != "admin":
        return redirect(url_for('index'))

    print(id)
    user.delete_user(id)

    flash("yeet", 'warning')
    return redirect(url_for('admin'))        


@app.route("/teapot") #test
def test():
    return render_template("test.html"), 418       

if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)
