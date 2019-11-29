import flask.globals
import flask.templating
from flask import Blueprint

import flaskblog.models.post_model as flaskblog_post

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
@main.route("/index")
def home():
    """Flask route representing the home page
    """
    page = flask.globals.request.args.get("page", 1, type=int)
    posts = flaskblog_post.Post.query.order_by(
        flaskblog_post.Post.date_posted.desc()
    ).paginate(page=page, per_page=5)
    return flask.templating.render_template(
        "home.html.j2", posts=posts, title="Home"
    )


@main.route("/about")
def about():
    """Flask route representing the about page
    """
    return flask.templating.render_template("about.html.j2", title="About")
