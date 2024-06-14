from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user

from .models.game import Game

from . import db

main = Blueprint('main', __name__)

@main.route("/")
def index():
    games = []

    db.execute('SELECT g.id, g.name, g.year, g."minPlayer", g."maxPlayer", g.age, g.length, g.user_id, g.category, u.favorite FROM games as g LEFT JOIN __game_user__ as u on g.id = u.game_id AND u.user_id = %s', (current_user.id,))
    for gameData in db:
        print(gameData)
        games.append(Game(gameData[0], gameData[1], gameData[2], gameData[3], gameData[4], gameData[5], gameData[6], gameData[7], gameData[8], gameData[9] if gameData[9] else False))

    print(games[0].category)
    # db.execute("SELECT * FROM games WHERE user_id IS NULL")
    # for gameData in db:
    #     games.append(Game(gameData[0], gameData[1], gameData[2], gameData[3], gameData[4], gameData[5], gameData[6], gameData[7], gameData[8]))

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
    return render_template("profile.html", name=current_user.name, games=current_user.games, favoriteGames=current_user.favoriteGames)


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

@main.route("/add_favorite/<gameId>")
@login_required
def add_favorite(gameId):
    db.execute("INSERT INTO __game_user__ as g (user_id, game_id, favorite) VALUES (%s, %s, TRUE) ON CONFLICT(user_id, game_id) DO UPDATE SET favorite = TRUE WHERE g.game_id = %s", (current_user.id, gameId, gameId))

    return redirect(request.referrer)

@main.route("/remove_favorite/<gameId>")
@login_required
def remove_favorite(gameId):
    db.execute("UPDATE __game_user__ SET favorite = FALSE WHERE game_id = %s AND user_id = %s", (gameId, current_user.id))

    return redirect(request.referrer)

def obj_dict(obj):
    return obj.__dict__
