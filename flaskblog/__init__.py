from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from flaskblog.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
mail = Mail()


def create_app(config_class=Config):
    """Creates the app and initializes the config of the app

    Parameters
    ----------

    config_class : Object, optional

        Manage the app setup settings, by default Config
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Needs to be imported here to resolve circular imports.
    from flaskblog.controller.user_controller import users  # noqa
    from flaskblog.controller.general_controller import main  # noqa
    from flaskblog.controller.posts_controller import posts  # noqa
    from flaskblog.controller.error_pages_controller import errors  # noqa

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
