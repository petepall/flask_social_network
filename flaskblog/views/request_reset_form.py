from flask_wtf.form import FlaskForm
from wtforms.ext.sqlalchemy.fields import ValidationError
from wtforms.fields.core import StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Email

from flaskblog.models.user_model import User


class RequestResetForm(FlaskForm):
    """Class representing the user password reset request form for the
    application

    Parameters
    ----------
    FlaskForm : WTForms

        Flask wtf class that is extended to create the user login form
    """

    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request password reset")

    def validate_email(self, email):
        """Validate if the given email is still available against the DB

        Parameters
        ----------
        email : string

            email as entered in the form.
        """
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                "There is no account with this email. You must register first."
            )
