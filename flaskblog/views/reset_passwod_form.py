import flask_wtf.form
import wtforms.fields.simple as wtforms_simple
import wtforms.validators


class ResetPasswordForm(flask_wtf.form.FlaskForm):
    """Class representing the password reset form for the application

    Parameters
    ----------
    FlaskForm : WTForms

        Flask wtf class that is extended to create the user login form
    """

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
    submit = wtforms_simple.SubmitField("Reset password")
