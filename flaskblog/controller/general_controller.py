from flask.templating import render_template

from flaskblog import app
from flaskblog.models.post_model import Post


@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    posts = Post.query.all()
    return render_template("home.html.j2", posts=posts, title="Home")


@app.route("/about")
def about():
    return render_template("about.html.j2", title="About")
