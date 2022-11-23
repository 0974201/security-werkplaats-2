from flask import Flask, render_template

# LISTEN_ALL = "0.0.0.0"
#FLASK_IP = LISTEN_ALL
#FLASK_PORT = 81
#FLASK_DEBUG = True

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')
    
app.run(debug=True)


    



