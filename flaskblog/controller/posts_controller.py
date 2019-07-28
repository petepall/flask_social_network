from flask import redirect
from flask.helpers import flash, url_for
from flask.templating import render_template
from flask_login import current_user, login_required

from flaskblog import app, db
from flaskblog.models.post_model import Post
from flaskblog.views.post_form import PostForm


@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            author=current_user,
        )
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", "success")
        return redirect(url_for("home"))
    return render_template("create_post.html.j2", title="New post", form=form)
