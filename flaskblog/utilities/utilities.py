import os
import secrets
from builtins import FileNotFoundError

from PIL import Image

from flaskblog import app


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, "static/profile_pics", picture_fn
    )
    output_size = (125, 125)
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(picture_path)
    return picture_fn


def delete_picture_file(picture_file):
    picture_path = os.path.join(
        app.root_path, "static/profile_pics", picture_file
    )
    if picture_file != "default.jpg":
        try:
            os.remove(picture_path)
        except FileNotFoundError:
            pass
