from flask import Flask, render_template, url_for, request, redirect, g
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3 

app = Flask(__name__)

class VragenModel:
    def __init__(self, database_file):
        self.database_file = database_file

    def run_query(self, sql_query):
        conn = sqlite3.connect(self.database_file)
        c = conn.cursor()
        c.execute(sql_query)
        tables = c.fetchall()
        conn.close()
        return tables

    def get_tables(self):
        sql_query = "SELECT name FROM sqlite_master WHERE type='table';"
        result = self.run_query(sql_query)
        table_list = []
        for table in result:
            table_list.append(table[0])
        return table_list

    def get_columns(self, table):
        sql_query = "PRAGMA table_info({})".format(table)
        result = self.run_query(sql_query)
        table_list = []
        for table in result:
            table_list.append(table[1])
        return table_list

table_list = []
    for table in result:
    table_list.append(table[0])
    return table_list

def get_unconvertable_values(self, table_name, column_name, datatype):
        sql_query = "SELECT id, " + column_name + " FROM " + table_name
        results = self.run_query(sql_query)
        unconvertable_values = []
        for result in results:
            if datatype == "boolean":
                if result[1] != "0" and result[1] != "1":
                    unconvertable_values.append(result)
        return unconvertable_values




# @app.route("/")
# def index():
#     data = get_db()
#     return str(data)

# def get_db():
#         db = getattr(g, "_database", None)
#         if db is None:
#             db = g._database = sqlite3.connect("databases/testcorrect_vragen.db")
#             cursor = db.cursor()
#             cursor. execute("select auteur from vragen")

#         return cursor.fetchall()

# if __name__ == "__main__":
#         app.run(debug=True)






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







    



