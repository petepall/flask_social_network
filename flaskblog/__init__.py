from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SECRET_KEY"] = "956b91dcad619e1d5137ee2fc1e14bc2"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/site.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

# Needs to be imported here to resolve circular imports.
# from flaskblog.controller import routes
from flaskblog.controller import (  # noqa  Discable check
    general_controller,
    user_controller,
    posts_controller,
)
