from flask import Flask
from flask_login import LoginManager, logout_user

from .models.game import Game
from .models.user import User
import psycopg2


db_connection = psycopg2.connect(database="postgres", host="aws-0-eu-west-2.pooler.supabase.com", user="postgres.optjmcvhmhzwmirhxxre", password="sAxk01I0z1OtzrUr", port="6543")
db = db_connection.cursor()
db_connection.autocommit = True


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "ludotheque-ing2-sql"

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        db.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
        user_data = db.fetchone()

        user = User(user_data[0], user_data[1], user_data[2], user_data[3], [])

        db.execute("SELECT * FROM games WHERE user_id = %s;", (user_id,))
        for gameData in db:
            user.games.append(Game(gameData[0], gameData[1], gameData[2], gameData[3], gameData[4], gameData[5], gameData[6], gameData[7], gameData[8]))

        return user

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app