from flask import Flask, render_template

app = Flask(__name__)
# safe = maakt dikgedrukte letters
# capitalize = geeft de eerste letter van een woord een hoofletter
# lower = maakt kleine letters
# upper = maakt alle letter hoofd letters
# title = die geeft een hoofletter aan elke woord
# trim = haalt lege spaces weg
# striptags= haalt html tags weg
# {{}} = dit is om python data  in html te zetten
# {% %} = dit is om python functies in html te zetten
# met </br> aan het einde van een html line kan je zinnen of woorden onder elkaar zetten
@app.route("/")
def index():
    first_name = "Nizar"
    stuff = "This is bold text"

    favorite_pizza = ["Pepperoni", "cheese", "Mashrooms", 41]
    return render_template(
        "index.html", first_name=first_name, stuff=stuff, favorite_pizza=favorite_pizza
    )


@app.route("/users/<name>")
def user(name):
    return render_template("user.html", user_name=name)


if __name__ == "__main__":
    app.run(debug=True)
