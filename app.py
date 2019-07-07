from flask import flash, Flask, g, redirect, render_template, url_for
from flask_login.login_manager import LoginManager
from peewee import DoesNotExist

from models import user
from models.base_model import DB
from models.user import User
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
    if form.valid_on_submit():
        flash("Yay, you registered!", "success")
        User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        return redirect(url_for("index"))
    return render_template("register.html", form=form)


@app.route("/")
def index():
    return "Hey"


if __name__ == "__main__":
    user.initialize()
    User.create_user(
        username="petepall",
        email="peter@ppallen.be",
        password="strike",
        admin=True,
    )
    app.run(debug=DEBUG)
