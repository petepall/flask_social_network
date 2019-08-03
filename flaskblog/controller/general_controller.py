from flask.globals import request
from flask.templating import render_template

from flaskblog import app
from flaskblog.models.post_model import Post


@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.paginate(page=page, per_page=5)
    return render_template("home.html.j2", posts=posts, title="Home")


@app.route("/about")
def about():
    return render_template("about.html.j2", title="About")
