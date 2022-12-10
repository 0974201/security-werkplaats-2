import os.path
import sqlite3
import sys

from flask import Flask, render_template



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
        rows, column_names = dbm.get_table_content(table_name)
        return render_template(
            "id.html", rows=rows, columns=column_names, table_name=table_name
        )

if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)






# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# db = SQLAlchemy(app)

# class todo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(200), nullable=False)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)

#     def __repr__(self):
#         return '(Tasks: %r)' % self.id


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         task_content= request.form.form['content']
#         new_task= todo(content=task_content)

#         try:
#             db.session.add(new_task)
#             db.session.commit()
#             return redirect('/')
#         except: 
#             return 'There was an issue adding your task'

#     else:
#         task= todo.query.order_by(todo.date_created).all()
#         return render_template('index.html', task=task)

# @app.route('/delete/<int:id>')
# def delete(id):
#     task_do_delete= todo.query.get_or_404(id)

#     try:
#         db.session.delete(task_do_delete)
#         db.session.commit()
#         return redirect('/')    
#     except:
#         return 'There was an issue deleting your task'

# @app.route('/update/<int:id>', method=['GET', 'POST'])
# def update(id):
#     task= todo.query.get_or_404(id)

#     if request.method == 'POST':
#         task.content = request.form['content']

#         try:
#             db.session.add(task)
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'There was an issue updating your task'      

#     else:
#         return render_template('index.html', task=task)
        
    
# if __name__ == "__main__":
#     app.run(debug=True)

# @app.route('/login')
# def login():
#     return render_template('login.html')







    



