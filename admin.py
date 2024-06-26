from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash

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
        game = Game(game_data[0], game_data[1], game_data[2], game_data[3], game_data[4], game_data[5], game_data[6], game_data[7], game_data[8])
        db.execute('SELECT AVG(grade), COUNT(grade) FROM __game_user__ WHERE game_id = %s', (game.id,))
        gradeData = db.fetchone()
        game.grade = gradeData[0] if gradeData[0] is not None else 0
        game.gradeCount = gradeData[1]
        games.append(game)

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
@admin.route("/delete_game_confirm/<uuid>")
def delete_game_confirm(uuid):
    if not current_user.admin:
        return redirect(url_for('main.profile'))
    
    db.execute("SELECT * FROM games WHERE id = %s;", (uuid,))
    gameData = db.fetchone()

    game = Game(gameData[0], gameData[1], gameData[2], gameData[3], gameData[4], gameData[5], gameData[6], gameData[7], gameData[8])

    return render_template("delete_game_confirmation.html", game=game)

@login_required
@admin.route("/delete_game_confirm/<uuid>", methods=["POST"])
def delete_game_confirm_post(uuid):
    if not current_user.admin:
        return redirect(url_for('main.profile'))
    
    db.execute("DELETE FROM games WHERE id = %s", (uuid,))

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

@login_required
@admin.route("/edit_user/<user_id>")
def edit_user(user_id):
    if not current_user.admin:
        return redirect(url_for('main.profile'))
    db.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
    user_data = db.fetchone()

    user = User(user_data[0], user_data[1], user_data[2], user_data[3], [], user_data[4])
    
    return render_template("edit_user.html", user=user)

@login_required
@admin.route("/edit_user/<user_id>", methods=["POST"])
def edit_user_post(user_id):
    if not current_user.admin:
        return redirect(url_for('main.profile'))
    
    if request.form.get("email"):
        db.execute("UPDATE users SET email = %s WHERE id = %s", (request.form.get("email"), user_id))
    
    if request.form.get("name"):
        db.execute("UPDATE users SET name = %s WHERE id = %s;", (request.form.get("name"), user_id))

    if request.form.get("admin"):
        db.execute("UPDATE users SET admin = TRUE WHERE id = %s", (user_id,))
    else:
        db.execute("UPDATE users SET admin = FALSE WHERE id = %s", (user_id,))
        
    return redirect(url_for("admin.main"))

@login_required
@admin.route("/create_user")
def create_user():
    if not current_user.admin:
        return redirect(url_for('main.profile'))

    return render_template("create_user.html")

@login_required
@admin.route("/create_user", methods=["POST"])
def create_user_post():
    if not current_user.admin:
        return redirect(url_for('main.profile'))
    
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")
    admin = True if request.form.get("admin") else False

    db.execute("SELECT * FROM users WHERE email = %s;", (email,))

    if len(db.fetchall()) > 0:
        flash("Un utilisateur avec cette addresse e-mail existe déjà.")
        return redirect(url_for('admin.create_user'))

    db.execute("INSERT INTO users (email, name, password, admin) VALUES (%s, %s, %s, %s)", (email, name, generate_password_hash(password), admin))

    return redirect(url_for("admin.main"))


@login_required
@admin.route("/create_game")
def create_game():
    if not current_user.admin:
        return redirect(url_for('main.profile'))

    return render_template("create_game.html")

@login_required
@admin.route("/create_game", methods=["POST"])
def create_game_post():
    if not current_user.admin:
        return redirect(url_for('main.profile'))
    
    name = request.form.get("name")
    category = request.form.get("category")
    length = request.form.get("length")
    minPlayer = request.form.get("minPlayer")
    maxPlayer = request.form.get("maxPlayer")
    age = request.form.get("age")
    year = request.form.get("year")

    db.execute('INSERT INTO games (name, category, year, "minPlayer", "maxPlayer", age, length) VALUES (%s, %s, %s, %s, %s, %s, %s)', (name, category, year, minPlayer, maxPlayer, age, length))

    return redirect(url_for("admin.main"))