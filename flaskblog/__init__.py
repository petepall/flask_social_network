from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SECRET_KEY"] = "956b91dcad619e1d5137ee2fc1e14bc2"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/site.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Needs to be imported here to resolve circular imports.
from flaskblog.controller import routes
