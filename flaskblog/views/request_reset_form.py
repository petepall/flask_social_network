from flask_wtf.form import FlaskForm
from wtforms.ext.sqlalchemy.fields import ValidationError
from wtforms.fields.core import StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Email

from flaskblog.models.user_model import User


class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request password reset")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                "There is no account with this email. You must register first."
            )
