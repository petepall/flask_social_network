from flask import Blueprint, abort, redirect, request
from flask.helpers import flash, url_for
from flask.templating import render_template
from flask_login import current_user, login_required

from flaskblog import db
from flaskblog.models.post_model import Post
from flaskblog.models.user_model import User
from flaskblog.views.post_form import PostForm

posts = Blueprint("posts", __name__)


@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    """Route for handling new blog posts
    """
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
        return redirect(url_for("main.home"))
    return render_template(
        "create_post.html.j2", title="New post", form=form, legend="New post"
    )


@posts.route("/post/<int:post_id>")
def post(post_id):
    """Shows a specific posts data
    
    :param post_id: ID number of the blog post
    :type post_id: int
    """
    post = Post.query.get_or_404(post_id)
    return render_template("post.html.j2", title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated!", "success")
        return redirect(url_for("posts.post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content

    return render_template(
        "create_post.html.j2",
        title="Update post",
        form=form,
        legend="Update post",
    )


@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", "success")
    return redirect(url_for("main.home"))


@posts.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = (
        Post.query.filter_by(author=user)
        .order_by(Post.date_posted.desc())
        .paginate(page=page, per_page=5)
    )
    return render_template(
        "user_posts.html.j2", posts=posts, user=user, title="User posts"
    )
