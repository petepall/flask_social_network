from flask import Blueprint
from flask.globals import request
from flask.templating import render_template

from flaskblog.models.post_model import Post

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
@main.route("/index")
def home():
    """Flask route representing the home page
    """
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(
        page=page, per_page=5
    )
    return render_template("home.html.j2", posts=posts, title="Home")


@main.route("/about")
def about():
    """Flask route representing the about page
    """
    return render_template("about.html.j2", title="About")
