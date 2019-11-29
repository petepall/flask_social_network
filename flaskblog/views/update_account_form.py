import flask_login
import flask_wtf
import flask_wtf.file as flask_file
import wtforms.fields.core as wtforms_core
import wtforms.fields.simple as wtforms_simple
import wtforms.validators

import flaskblog.models.user_model as flaskblog_user


class UpdateAccountForm(flask_wtf.FlaskForm):
    """Class representing the account update form for the application

    Parameters
    ----------
    FlaskForm : WTForms

        Flask wtf class that is extended to create the user login form
    """

    username = wtforms_core.StringField(
        "Username",
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min=2, max=20),
        ],
    )
    email = wtforms_core.StringField(
        "Email",
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Email(),
        ],
    )
    picture = flask_file.FileField(
        "Update profile picture",
        validators=[flask_file.FileAllowed(["jpg", "png"])],
    )
    submit = wtforms_simple.SubmitField("Update")

    def validate_username(self, username):
        """Validate if the given username is still available against the DB

        Parameters
        ----------
        username : string

            Username as entered in the form.
        """
        if username.data != flask_login.current_user.username:
            user = flaskblog_user.User.query.filter_by(
                username=username.data
            ).first()
            if user:
                raise wtforms.validators.ValidationError(
                    "That username is taken. Please choose a different one"
                )

    def validate_email(self, email):
        """Validate if the given email is still available against the DB

        Parameters
        ----------
        email : string

            email as entered in the form.
        """
        if email.data != flask_login.current_user.email:
            user = flaskblog_user.User.query.filter_by(
                email=email.data
            ).first()
            if user:
                raise wtforms.validators.ValidationError(
                    "That email address is taken. Please choose a different one"
                )
