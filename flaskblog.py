from datetime import datetime

from flask import Flask, redirect
from flask.helpers import flash, url_for
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy

from forms import LoginForm, RegistrationForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "956b91dcad619e1d5137ee2fc1e14bc2"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/site.db"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(
        db.String(20), nullable=False, default="default,jpg"
    )
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


posts = [
    {
        "author": "Peter Pallen",
        "title": "Blog post 1",
        "content": "First post content",
        "date_posted": "July 20, 2019",
    },
    {
        "author": "Carine Pallen",
        "title": "Blog post 2",
        "content": "Second post content",
        "date_posted": "July 21, 2019",
    },
]


@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    return render_template("home.html.j2", posts=posts, title="Home")


@app.route("/about")
def about():
    return render_template("about.html.j2", title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data.upper()}!", "success")
        return redirect(url_for("home"))
    return render_template("register.html.j2", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if (
            form.email.data == "admin@blog.com"
            and form.password.data == "strike"
        ):
            flash("You have been logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash(
                "Login unsuccessful. Please check username and password",
                "danger",
            )
    return render_template("login.html.j2", title="Login", form=form)


if __name__ == "__main__":
    app.run(host="localhost", debug=True)
