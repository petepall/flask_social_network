import builtins
import os
import secrets
import smtplib

import flask.globals
import flask.helpers
import flask_mail
from PIL import Image

import flaskblog


def save_picture(form_picture):
    """Funtion to save profile picture to disk with standardized filename

    Parameters
    ----------
    form_picture : object

        Picture data including the filename
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        flask.globals.current_app.root_path, "static/profile_pics", picture_fn
    )
    image = resize_picture(form_picture)
    image.save(picture_path)
    return picture_fn


def resize_picture(form_picture):
    """Resizing of a given picture to format of 125 x 125

    :param form_picture: Picture data
    :type form_picture: object
    """
    output_size = (125, 125)
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    return image


def delete_picture_file(picture_file):
    """Delete the given picture file from the disk if it exists

    Parameters
    ----------
    picture_file : string

        Delete the picture with the given filename from the disk
    """
    picture_path = os.path.join(
        flask.globals.current_app.root_path,
        "static/profile_pics",
        picture_file,
    )
    if picture_file != "default.jpg":
        try:
            os.remove(picture_path)
        except builtins.FileNotFoundError:
            pass


def send_reset_email(user):
    """Send a reset email to a user

    Parameters
    ----------
    user : User

        User object containing the data of a User including the email address
    """
    token = user.get_reset_token()
    msg = flask_mail.Message(
        "Password reset request",
        sender="noreply@demo.com",
        recipients=[user.email],
    )
    msg.body = f"""To reset your password, visit the following link:
{flask.helpers.url_for('users.reset_token', token=token, _external=True)}
    
If you did not make this request, then simply ignore this email and no change will be done 
"""  # noqa
    try:
        flaskblog.mail.send(msg)
    except smtplib.SMTPAuthenticationError as err:
        flask.helpers.flash(f"The authentication failed {err}")
