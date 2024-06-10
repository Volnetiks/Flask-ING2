from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required

from .models.game import Game
from .models.user import User
from . import db

admin = Blueprint("admin", __name__)

@login_required
@admin.route("/main")
def main():
    if not current_user.admin:
        return redirect(url_for('main.profile'))

    db.execute("SELECT * FROM users")
    users_data = db.fetchall()
    db.execute("SELECT * FROM games")
    games_data = db.fetchall()
    users = []
    games = []

    for user_data in users_data:
        user = User(user_data[0], user_data[1], user_data[2], user_data[3], [], user_data[4])
        db.execute("SELECT * FROM games WHERE user_id = %s;", (user.id,))

        for game_data in db:
            user.games.append(Game(game_data[0], game_data[1], game_data[2], game_data[3], game_data[4], game_data[5], game_data[6], game_data[7], game_data[8]))

        users.append(user)   

    for game_data in games_data:
        games.append(Game(game_data[0], game_data[1], game_data[2], game_data[3], game_data[4], game_data[5], game_data[6], game_data[7], game_data[8]))

    return render_template("main_admin.html", users=users, name=current_user.name, games=games)


@login_required
@admin.route("/delete_user_confirm/<uuid>")
def delete_user_confirm(uuid):
    if not current_user.admin:
        return redirect(url_for('main.profile'))
    
    db.execute("SELECT * FROM users WHERE id = %s;", (uuid,))
    user_data = db.fetchone()

    user = User(user_data[0], user_data[1], user_data[2], user_data[3], [], user_data[4])

    return render_template("delete_user_confirmation.html", user=user)

@login_required
@admin.route("/delete_user_confirm/<uuid>", methods=["POST"])
def delete_user_confirm_post(uuid):
    if not current_user.admin:
        return redirect(url_for('main.profile'))
    
    db.execute("UPDATE games SET user_id = NULL WHERE user_id = %s;", (uuid,))
    db.execute("DELETE FROM users WHERE id = %s", (uuid,))

    return redirect(url_for("admin.main"))

@login_required
@admin.route("/edit_game/<game_id>")
def edit_game(game_id):
    if not current_user.admin:
        return redirect(url_for('main.profile'))
    
    db.execute("SELECT * FROM games WHERE id = %s;", (game_id,))
    game_data = db.fetchone()

    game = Game(game_data[0], game_data[1], game_data[2], game_data[3], game_data[4], game_data[5], game_data[6], game_data[7], game_data[8])
    
    return render_template("edit_game.html", game=game)

@login_required
@admin.route("/edit_game/<game_id>", methods=["POST"])
def edit_game_post(game_id):
    if not current_user.admin:
        return redirect(url_for('main.profile'))
        
    if request.form.get("name"):
        db.execute("UPDATE games SET name = %s WHERE id = %s;", (request.form.get("name"), game_id))

    if request.form.get("category"):
        db.execute("UPDATE games SET category = %s WHERE id = %s;", (request.form.get("category"), game_id))

    if request.form.get("year"):
        db.execute('UPDATE games SET year = %s WHERE id = %s;', (request.form.get("year"), game_id))

    if request.form.get("minPlayer"):
        db.execute('UPDATE games SET "minPlayer" = %s WHERE id = %s;', (request.form.get("minPlayer"), game_id))

    if request.form.get("maxPlayer"):
        db.execute('UPDATE games SET "maxPlayer" = %s WHERE id = %s;', (request.form.get("maxPlayer"), game_id))

    if request.form.get("age"):
        db.execute("UPDATE games SET age = %s WHERE id = %s;", (request.form.get("age"), game_id))

    if request.form.get("length"):
        db.execute("UPDATE games SET length = %s WHERE id = %s;", (request.form.get("length"), game_id))

    return redirect(url_for("admin.main"))