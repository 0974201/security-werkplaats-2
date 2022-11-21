from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Create a Flask instance
app = Flask(__name__)
app.config["SECRET_KEY"] = "yep this is a secret key very special indeed hihihi"

# Creat a form Class
class NamerForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


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


@app.route("/name", methods=["GET", "POST"])
def name():
    name = None
    form = NamerForm()
    # Validate form input on submit
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
    return render_template("name.html", name=name, form=form)


# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500
