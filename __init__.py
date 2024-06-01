import json
from flask import Flask
from flask_login import LoginManager
from .models.user import recuperer_uilisateur


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "caca"

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        user = recuperer_uilisateur(user_id)
        print(user_id)
        print(user)

        return user

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
