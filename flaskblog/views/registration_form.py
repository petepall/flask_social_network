from flask_wtf import FlaskForm
from wtforms.fields.core import StringField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    ValidationError,
)
from flaskblog.models.user_model import User


class RegistrationForm(FlaskForm):
    """Class representing the registration form for the application

    Parameters
    ----------
    FlaskForm : WTForms

        Flask wtf class that is extended to create the user login form
    """

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        """Validate if the given username is still available against the DB

        Parameters
        ----------
        username : string

            Username as entered in the form.
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "That username is taken. Please choose a different one"
            )

    def validate_email(self, email):
        """Validate if the given email is still available against the DB

        Parameters
        ----------
        email : string

            email as entered in the form.
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "That email address is taken. Please choose a different one"
            )
