from flask import Flask, render_template, url_for, request, Redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['sqalchemy_database_uri'] = 'sqlite:///tesy.db'
db = SQLAlchemy(app)

class todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '(Tasks: %r)' % self.id


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content= request.form.form['content']
        new_task= todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        task= todo.query.order_by(todo.date_created).all()
        return render_template('index.html', task=task)

@app.route('/delete/<int:id>')
def delete(id):
    task_do_delete= todo.query.get_or_404(id)

    try:
        db.session.delete(task_do_delete)
        db.session.commit()
        return redirect('/')    
    except:
        return 'There was an issue deleting your task'

@app.route('/update/<int:id>', method=['GET', 'POST'])
def update(id):
    task= todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.add(task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'      

    else:
        return render_template('update.html', task=task=)
        
    
if __name__ == "__main__":
    app.run(debug=True)
    
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')







    



