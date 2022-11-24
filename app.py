from flask import Flask, render_template

app = Flask(__name__)
# safe =
# capitalize
# lower
# upper
# title
# trim
# striptags
@app.route("/")
def index():
    first_name = "Nizar"
    stuff = "This is <strong> Bold</strong> Text"

    return render_template("index.html", first_name=first_name, stuff=stuff)


@app.route("/users/<name>")
def user(name):
    return render_template("user.html", user_name=name)


if __name__ == "__main__":
    app.run(debug=True)
