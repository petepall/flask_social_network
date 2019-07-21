from flask import Flask, redirect
from flask.helpers import flash, url_for
from flask.templating import render_template

from forms import LoginForm, RegistrationForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "956b91dcad619e1d5137ee2fc1e14bc2"

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


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home"))
    return render_template("register.html.j2", title="Register", form=form)


@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html.j2", title="Login", form=form)


if __name__ == "__main__":
    app.run(host="localhost", debug=True)
