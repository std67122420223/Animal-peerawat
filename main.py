from flask import Flask, render_template, request, redirect

app = Flask(__name__)

animals = [{"id":1,"name":"Tiger","species":"Mammal","habitat":"Land","legs":4},
{"id":2,"name":"Eagle","species":"Bird","habitat":"Land","legs":2},
{"id":3,"name":"Shark","species":"Fish","habitat":"Water","legs":0}]

@app.route("/")
def home():
    return redirect("/animals")


@app.route("/animals")
def animal_list():
    search = request.args.get("search","")

    if search:
        filtered = [a for a in animals if search.lower() in a["name"].lower()]
    else:
        filtered = animals

    return render_template("animals.html", animals=filtered)


@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        species = request.form["species"]
        habitat = request.form["habitat"]

        animal = {
            "id": len(animals)+1,
            "name": name,
            "species": species,
            "habitat": habitat,
            "legs": int(request.form["legs"])
        }

        animals.append(animal)

        return redirect("/animals")

    return render_template("add.html")


@app.route("/delete/<int:id>")
def delete(id):
    global animals
    animals = [a for a in animals if a["id"] != id]
    return redirect("/animals")


@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id):

    animal = None
    for a in animals:
        if a["id"] == id:
            animal = a

    if request.method == "POST":
        animal["name"] = request.form["name"]
        animal["species"] = request.form["species"]
        animal["habitat"] = request.form["habitat"]
        animal["legs"] = int(request.form["legs"])
        return redirect("/animals")

    return render_template("edit.html", animal=animal)


if __name__ == "__main__":
    app.run(debug=True)