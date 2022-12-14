import os.path
import sqlite3
import sys

from flask import Flask, render_template, request



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
DATABASE_FILE = os.path.join(app.root_path, 'databases', 'testcorrect_vragen.db')

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
def index():
    tables = dbm.get_table_list()
    return render_template(
        "tables.html", table_list=tables, database_file=DATABASE_FILE
    )


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
@app.route("/id/<table_name>")
def id_html(table_name=None):
    if not table_name:
        return "Missing table name", 400  # HTTP 400 = Bad Request
    else:
        rows, column_names = dbm.get_id_html(table_name, "id.html" , "vragen" )
        return render_template(
            "id.html", rows=rows, columns=column_names, table_name=table_name)


@app.route("/leerdoel/<table_name>")
def leerdoel_html(table_name=None):
    if not table_name:
        return "Missing table name", 400  # HTTP 400 = Bad Request
    else:
        rows, column_names = dbm.get_leerdoel_html(table_name, "leerdoel.html" , "vragen" )
        return render_template(
            "leerdoel.html", rows=rows, columns=column_names, table_name=table_name)
@app.route("/vraag/<table_name>")
def vraag_html(table_name=None):
    if not table_name:
        return "Missing table name", 400  # HTTP 400 = Bad Request
    else:
        rows, column_names = dbm.get_vraag_html(table_name, "vraag.html" , "vragen" )
        return render_template(
            "vraag.html", rows=rows, columns=column_names, table_name=table_name)

@app.route("/auteur/<table_name>")
def auteur_html(table_name=None):
    if not table_name:
        return "Missing table name", 400  # HTTP 400 = Bad Request
    else:
        rows, column_names = dbm.get_auteur_html(table_name, "auteur.html" , "vragen" )
        return render_template(
            "auteur.html", rows=rows, columns=column_names, table_name=table_name)
# @app.route(table_content, methods= ['GET', 'POST'])
#
# def tabledata(columns):
#     if request.method == "POST":
#         col = request.form.get('column')
#
#     else:
#         columns = ['vraag']
#         columnslist = ['vraag', 'leerdoel', 'id']
#         data = table_content(columns)
#     return render_template("table_details.html", data = data, columns = columnslist)

if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)









    



