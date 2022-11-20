from flask import Flask, render_template

# Create a Flask instance
app = Flask(__name__)

# Define a route for the default URL, which loads the form
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/user/<username>")
def user(username):
    return "Hello, {}!".format(username)
