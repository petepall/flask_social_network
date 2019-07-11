"""UserID and password for testing:
email: peter.pallen@gmail.com
pass: strike
"""
from flask import Flask, flash, g, redirect, render_template, url_for
from flask_bcrypt import check_password_hash
from flask_login import login_user
from flask_login.login_manager import LoginManager
from peewee import DoesNotExist

from models.base_model import DB
from models.user import User
from views.login_form import LoginForm
from views.register_form import RegisterForm

DEBUG = True

app = Flask(__name__)
app.secret_key = "ksjdk3kj3r3$34#4emfke#$3fel,s,dm2;#fkjdkj3$#$#dsldsj232@@^&*"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(userid):
    try:
        return User.get(User.id == userid)
    except DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request
    """
    g.db = DB
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database after each request
    """
    g.db.close()
    return response


@app.route("/register", methods=("GET", "POST"))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash("Yay, you registered!", "success")
        User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        return redirect(url_for("index"))
    return render_template("register.html", form=form)


@app.route("/login", methods=("GET", "POST"))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.get(User.email == form.email.data)
        except DoesNotExist:
            flash("Your email or password does not match", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You have been logged in!", "success")
                return redirect(url_for("index"))
            else:
                flash("Your email or password does not match", "error")
    return render_template("login.html", form=form)


@app.route("/")
def index():
    return "Hey"


def initialize():
    DB.connect(reuse_if_open=True)
    DB.create_tables([User], safe=True)
    DB.close()


if __name__ == "__main__":
    initialize()
    try:
        User.create_user(
            username="petepall",
            email="peter@ppallen.be",
            password="strike",
            admin=True,
        )
    except ValueError:
        pass
    app.run(debug=DEBUG)
