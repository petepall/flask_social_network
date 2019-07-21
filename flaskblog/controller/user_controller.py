from flask import redirect
from flask.helpers import flash, url_for
from flask.templating import render_template
from flask_login import current_user, login_user, logout_user

from flaskblog import app, bcrypt, db
from flaskblog.models.post_model import Post
from flaskblog.models.user_model import User
from flaskblog.views.login_form import LoginForm
from flaskblog.views.registration_form import RegistrationForm


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode("utf-8")
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        flash(
            f"Account created for {form.username.data.upper()}! "
            f"You are now able to log in",
            "success",
        )
        return redirect(url_for("login"))
    return render_template("register.html.j2", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
            user.password, form.password.data
        ):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("home"))
        else:
            flash(
                "Login unsuccessful. Please check username and password",
                "danger",
            )
    return render_template("login.html.j2", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))
