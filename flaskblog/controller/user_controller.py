from flask import redirect, request
from flask.helpers import flash, url_for
from flask.templating import render_template
from flask_login import current_user, login_required, login_user, logout_user

from flaskblog import app, bcrypt, db
from flaskblog.models.post_model import Post  # noqa
from flaskblog.models.user_model import User
from flaskblog.utilities.utilities import delete_picture_file, save_picture
from flaskblog.views.login_form import LoginForm
from flaskblog.views.registration_form import RegistrationForm
from flaskblog.views.request_reset_form import RequestResetForm
from flaskblog.views.reset_passwod_form import ResetPasswordForm
from flaskblog.views.update_account_form import UpdateAccountForm


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
            next_page = request.args.get("next")
            return (
                redirect(next_page) if next_page else redirect(url_for("home"))
            )
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


@app.route("/account", methods=["GET", "POST"])
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
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for(
        "static", filename="profile_pics/" + current_user.image_file
    )
    return render_template(
        "account.html.j2", title="Account", image_file=image_file, form=form
    )


@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RequestResetForm()
    return render_template(
        "reset_request.html.j2", title="Reset password", form=form
    )


