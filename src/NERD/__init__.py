import os

from flask import Flask
from flask_login import LoginManager

from NERD import config

from .auth import auth
from .models import User
from .views import views


def create_app():
    app = Flask(__name__)

    app.secret_key = "dev"

    app.config["BASE_PATH"] = os.path.dirname(__file__)
    app.config["STORAGE_PATH"] = config.STORAGE_PATH

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User()

    return app
