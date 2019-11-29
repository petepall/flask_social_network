import flask_wtf
import wtforms
import wtforms.fields.core as wtforms_core
import wtforms.fields.simple as wtforms_simple


class LoginForm(flask_wtf.FlaskForm):
    """Class representing the login form for the application

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
    password = wtforms_simple.PasswordField(
        "Password", validators=[wtforms.validators.DataRequired()]
    )
    remember = wtforms_core.BooleanField("Remember Me")
    submit = wtforms_simple.SubmitField("Login")
