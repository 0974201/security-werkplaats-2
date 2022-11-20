from flask import Flask, render_template

# Create a Flask instance
app = Flask(__name__)

# Define a route for the default URL, which loads the form
@app.route("/")
def index():
    name = "Jeroen"
    things = "Roses are red, violets are blue"
    fruits = ["apple", "banana", "orange", "pineapple"]
    return render_template("index.html", name=name, things=things, fruits=fruits)


@app.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name)
