from flask import Blueprint, render_template, request, redirect, session
from .models import Animal, User
from .extensions import db

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    if "user" not in session:
        return redirect("/login")

    search = request.args.get("search")

    if search:
        animals = Animal.query.filter(
            Animal.name.ilike(f"%{search}%")
        ).all()
    else:
        animals = Animal.query.order_by(Animal.id).all()

    return render_template("animals.html", animals=animals)


@main_bp.route("/add", methods=["GET","POST"])
def add():

    if request.method == "POST":

        animal = Animal(
            name=request.form["name"],
            species=request.form["species"],
            habitat=request.form["habitat"],
            legs=request.form["legs"]
        )

        db.session.add(animal)
        db.session.commit()

        return redirect("/")

    return render_template("add.html")
@main_bp.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id):

    animal = Animal.query.get_or_404(id)

    if request.method == "POST":
        animal.name = request.form["name"]
        animal.species = request.form["species"]
        animal.habitat = request.form["habitat"]
        animal.legs = request.form["legs"]

        db.session.commit()

        return redirect("/")

    return render_template("edit.html", animal=animal)
@main_bp.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
         return "Password not match"

        user = User(username=username, email=email, password=password)

        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")
@main_bp.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session["user"] = user.username
            return redirect("/")
        else:
            return "Login Failed"

    return render_template("login.html")
@main_bp.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/login")