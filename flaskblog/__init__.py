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

# Needs to be imported here to resolve circular imports.
# from flaskblog.controller import routes
from flaskblog.controller import general_controller, user_controller
