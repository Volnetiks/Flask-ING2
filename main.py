from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user

from .models.game import Game

from . import db

import json

main = Blueprint('main', __name__)

@main.route("/")
def index():
    games = []

    db.execute("SELECT * FROM games WHERE user_id IS NULL")
    for gameData in db:
        games.append(Game(gameData[0], gameData[1], gameData[2], gameData[3], gameData[4], gameData[5], gameData[6], gameData[7], gameData[8]))

    return render_template("index.html", games=games)


@main.route("/research", methods=["POST"])
def research():
    value = request.form.get("research")
    games = []
    db.execute("SELECT * FROM games WHERE name ILIKE %s", ("%" + value + "%",))

    for gameData in db:
        games.append(Game(gameData[0], gameData[1], gameData[2], gameData[3], gameData[4], gameData[5], gameData[6], gameData[7], gameData[8]))

    return render_template('research.html', games=games, value=value)


@main.route("/research")
def research_all():
    games = []

    db.execute("SELECT * FROM games WHERE user_id IS NULL")
    for gameData in db:
        games.append(Game(gameData[0], gameData[1], gameData[2], gameData[3], gameData[4], gameData[5], gameData[6], gameData[7], gameData[8]))

    return render_template('research.html', games=games)


@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name=current_user.name, games=current_user.games)


@main.route("/reservation_confirmation/<name>")
@login_required
def reservation_confirmation(name):
    db.execute("SELECT * FROM games WHERE name = %s;", (name,))

    gameData = db.fetchone()

    if gameData is None:
        return render_template("main.index")
    
    game = Game(gameData[0], gameData[1], gameData[2], gameData[3], gameData[4], gameData[5], gameData[6], gameData[7], gameData[8])

    return render_template("reservation_confirmation.html", game=game)


@main.route("/return_confirmation/<name>")
@login_required
def return_confirmation(name):
    db.execute("SELECT * FROM games WHERE name = %s;", (name,))

    gameData = db.fetchone()

    if gameData is None:
        return render_template("main.profile")
    
    game = Game(gameData[0], gameData[1], gameData[2], gameData[3], gameData[4], gameData[5], gameData[6], gameData[7], gameData[8])

    return render_template("return_confirmation.html", game=game)


@main.route("/reservation_confirmation/<name>", methods=["POST"])
@login_required
def reservation_confirmation_post(name):
    db.execute("UPDATE games SET user_id = %s WHERE name = %s", (current_user.id, name))

    return redirect(url_for("main.profile"))


@main.route("/return_confirmation/<name>", methods=["POST"])
@login_required
def return_confirmation_post(name):
    db.execute("UPDATE games SET user_id = NULL WHERE name = %s", (name,))

    return redirect(url_for("main.profile"))


def obj_dict(obj):
    return obj.__dict__
