from flask import Blueprint, render_template, redirect, url_for
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
    usersData = db.fetchall()
    users = []

    for user_data in usersData:
        user = User(user_data[0], user_data[1], user_data[2], user_data[3], [], user_data[4])
        db.execute("SELECT * FROM games WHERE user_id = %s;", (user.id,))

        for gameData in db:
            user.games.append(Game(gameData[0], gameData[1], gameData[2], gameData[3], gameData[4], gameData[5], gameData[6], gameData[7], gameData[8]))

        users.append(user)    

    return render_template("main_admin.html", users=users, name=current_user.name)


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