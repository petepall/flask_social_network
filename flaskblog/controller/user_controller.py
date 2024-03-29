from flask import Blueprint, redirect, request
from flask.helpers import flash, url_for
from flask.templating import render_template
from flask_login import current_user, login_required, login_user, logout_user

from flaskblog import bcrypt, db
from flaskblog.models.post_model import Post  # noqa
from flaskblog.models.user_model import User
from flaskblog.utilities.utilities import (
    delete_picture_file,
    save_picture,
    send_reset_email,
)
from flaskblog.views.login_form import LoginForm
from flaskblog.views.registration_form import RegistrationForm
from flaskblog.views.request_reset_form import RequestResetForm
from flaskblog.views.reset_passwod_form import ResetPasswordForm
from flaskblog.views.update_account_form import UpdateAccountForm

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
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
        return redirect(url_for("users.login"))
    return render_template("register.html.j2", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
            user.password, form.password.data
        ):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return (
                redirect(next_page)
                if next_page
                else redirect(url_for("main.home"))
            )
        else:
            flash(
                "Login unsuccessful. Please check username and password",
                "danger",
            )
    return render_template("login.html.j2", title="Login", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            delete_picture_file(current_user.image_file)
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for(
        "static", filename="profile_pics/" + current_user.image_file
    )
    return render_template(
        "account.html.j2", title="Account", image_file=image_file, form=form
    )


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(
            "An email has been send with instructions to reset your password",
            "info",
        )
        return redirect(url_for("users.login"))
    return render_template(
        "reset_request.html.j2", title="Reset password", form=form
    )


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("users.reset_request"))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash(
            f"Your password has been updated! " f"You are now able to log in",
            "success",
        )
        return redirect(url_for("users.login"))
    return render_template(
        "reset_token.html.j2", title="Reset password", form=form
    )
