from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user

from .models.jeu import Jeu
from .models.user import User
import json

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember_me = True if request.form.get("remember") else False
    user = None

    with open("./db/utilisateurs.json", "r") as f:
        utilisateursData = json.load(f)
        for utilisateurData in utilisateursData:
            if utilisateurData["email"] == email and utilisateurData["password"] == password:
                user = User(email, utilisateurData["name"],
                            password, int(utilisateurData["id"]), [Jeu(
                                jeu["nom"], jeu["categorie"], jeu["annee"], jeu["joueursmin"], jeu["joueursmax"], jeu["age"], jeu["duree"], jeu["disponible"]) for jeu in utilisateurData["jeux"]])
                login_user(user, remember=remember_me)

    if user == None:
        flash("Erreur dans les identifiants")
        return redirect(url_for("auth.login"))

    return redirect(url_for("main.profile"))


@auth.route("/signup")
def signup():
    return render_template("signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    users = []

    with open("./db/utilisateurs.json", "r") as f:
        utilisateursData = json.load(f)
        for utilisateurData in utilisateursData:
            id = utilisateurData["id"]
            users.append(User(
                utilisateurData["email"], utilisateurData["name"], utilisateurData["password"], id, []))
            if utilisateurData["email"] == email:
                flash("Cette addresse email est déjà utilisé")
                return redirect(url_for("auth.signup"))

    id = len(users) + 1

    with open("./db/utilisateurs.json", "w") as f:
        users.append(User(email, name, password, id))
        json.dump(users, f, indent=4, default=obj_dict)

    return redirect(url_for("auth.login"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


def obj_dict(obj):
    return obj.__dict__
