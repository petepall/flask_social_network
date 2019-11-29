import flask_wtf
import wtforms.fields.core as wtforms_core
import wtforms.fields.simple as wtforms_simple
import wtforms.validators

import flaskblog.models.user_model as flaskblog_user


class RegistrationForm(flask_wtf.FlaskForm):
    """Class representing the registration form for the application

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
    password = wtforms_simple.PasswordField(
        "Password", validators=[wtforms.validators.DataRequired()]
    )
    confirm_password = wtforms_simple.PasswordField(
        "Confirm Password",
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.EqualTo("password"),
        ],
    )
    submit = wtforms_simple.SubmitField("Sign Up")

    def validate_username(self, username):
        """Validate if the given username is still available against the DB

        Parameters
        ----------
        username : string

            Username as entered in the form.
        """
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
        user = flaskblog_user.User.query.filter_by(email=email.data).first()
        if user:
            raise wtforms.validators.ValidationError(
                "That email address is taken. Please choose a different one"
            )
