from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from .models.game import Game

from .models.user import User

from . import db, db_connection

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember_me = True if request.form.get("remember") else False

    db.execute("SELECT * FROM users WHERE email = %s;", (email,))

    user_data = db.fetchone()
    user = User(user_data[0], user_data[1], user_data[2], user_data[3], [], user_data[4])

    if not user or not check_password_hash(user.password, password):
        flash("Verifier vos identifiants.")
        return redirect(url_for('auth.login'))
    
    db.execute("SELECT * FROM games WHERE user_id = %s;", (user.id,))
    for gameData in db:
        user.games.append(Game(gameData[0], gameData[1], gameData[2], gameData[3], gameData[4], gameData[5], gameData[6], gameData[7], gameData[8]))

    login_user(user, remember=remember_me)
    return redirect(url_for("main.profile"))


@auth.route("/signup")
def signup():
    return render_template("signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    db.execute("SELECT * FROM users WHERE email = %s;", (email,))

    if len(db.fetchall()) > 0:
        flash("Un utilisateur avec cette addresse e-mail existe déjà.")
        return redirect(url_for('auth.signup'))

    db.execute("INSERT INTO users (email, name, password) VALUES (%s, %s, %s)", (email, name, generate_password_hash(password)))

    return redirect(url_for("auth.login"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


def obj_dict(obj):
    return obj.__dict__
