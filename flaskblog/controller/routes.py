from flask import redirect
from flask.helpers import flash, url_for
from flask.templating import render_template

from flaskblog import app
from flaskblog.views.login_form import LoginForm
from flaskblog.views.registration_form import RegistrationForm

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
