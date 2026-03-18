from flask import Blueprint, render_template, request, redirect, session
from werkzeug.utils import secure_filename
import os
from .models import Animal, User
from .extensions import db

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    if "user_id" not in session:
        return redirect("/login")

    search = request.args.get("search")

    if search:
        animals = Animal.query.filter(
            Animal.user_id == session["user_id"],
            Animal.name.ilike(f"%{search}%")
        ).all()
    else:
        animals = Animal.query.filter_by(
         user_id=session["user_id"]
        ).order_by(Animal.id).all()

    return render_template("animals.html", animals=animals)
@main_bp.route("/animals")
def animals():
    return redirect("/")
@main_bp.route("/add", methods=["GET","POST"])
def add():

    if request.method == "POST":
        animal = Animal(
            name=request.form["name"],
            species=request.form["species"],
            habitat=request.form["habitat"],
            legs=request.form["legs"],
            image=request.form["image_url"],
            user_id=session["user_id"]

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
        animal.image = request.form["image_url"]

        db.session.commit()

        return redirect("/")

    return render_template("edit.html", animal=animal)
@main_bp.route("/register", methods=["GET","POST"])
def register():
    error = None

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
         error = "Passwords do not match"
        else:
         user = User(username=username, email=email, password=password)

         db.session.add(user)
         db.session.commit()

         return redirect("/login")

    return render_template("register.html", error=error)
@main_bp.route("/login", methods=["GET","POST"])
def login():
    error = None 

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session["user_id"] = user.id
            return redirect("/")
        else:
            error = "Username or Password incorrect"

    return render_template("login.html", error=error)
@main_bp.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/login")
@main_bp.route("/change_password", methods=["GET","POST"])
def change_password():

    error = None

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        current_password = request.form["current_password"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        user = User.query.get(session["user_id"])

        if user.password != current_password:
            error = "Current password incorrect"

        elif new_password != confirm_password:
            error = "New passwords do not match"

        else:
            user.password = new_password
            db.session.commit()
            return redirect("/")

    return render_template("change_password.html", error=error)
@main_bp.route("/delete/<int:id>")
def delete(id):

    animal = Animal.query.get_or_404(id)

    db.session.delete(animal)
    db.session.commit()

    return redirect("/")