import flask_wtf.form
import wtforms.fields.core as wtforms_core
import wtforms.fields.simple as wtforms_simple
import wtforms.validators

import flaskblog.models.user_model as flaskblog_user


class RequestResetForm(flask_wtf.form.FlaskForm):
    """Class representing the user password reset request form for the
    application

    Parameters
    ----------
    FlaskForm : WTForms

        Flask wtf class that is extended to create the user login form
    """

    email = wtforms_core.StringField(
        "Email",
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Email(),
        ],
    )
    submit = wtforms_simple.SubmitField("Request password reset")

    def validate_email(self, email):
        """Validate if the given email is still available against the DB

        Parameters
        ----------
        email : string

            email as entered in the form.
        """
        user = flaskblog_user.User.query.filter_by(email=email.data).first()
        if user is None:
            raise wtforms.validators.ValidationError(
                "There is no account with this email. You must register first."
            )
