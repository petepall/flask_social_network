import flask_wtf
import wtforms.fields.core as wtforms_core
import wtforms.fields.simple as wtforms_simple
import wtforms.validators


class PostForm(flask_wtf.FlaskForm):
    """Class representing the blog post form for the application

    Parameters
    ----------
    FlaskForm : WTForms

        Flask wtf class that is extended to create the user login form
    """

    title = wtforms_core.StringField(
        "Title", validators=[wtforms.validators.DataRequired()]
    )
    content = wtforms_simple.TextAreaField(
        "Content", validators=[wtforms.validators.DataRequired()]
    )
    submit = wtforms_simple.SubmitField("Post")
