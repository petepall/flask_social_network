from flask.templating import render_template

from flaskblog import app

posts = [
    {
        "author": "Peter Pallen",
        "title": "Blog post 1",
        "content": "First post content",
        "date_posted": "July 20, 2019",
    },
    {
        "author": "Carine Pallen",
        "title": "Blog post 2",
        "content": "Second post content",
        "date_posted": "July 21, 2019",
    },
]


@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    return render_template("home.html.j2", posts=posts, title="Home")


@app.route("/about")
def about():
    return render_template("about.html.j2", title="About")
