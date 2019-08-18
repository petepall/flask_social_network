from datetime import datetime

from flaskblog import db


class Post(db.Model):
    """Class representing the Post table in the database

    Parameters
    ----------
    db : database object

        represents the database object.
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        """String representation of the post object
        """
        return f"Post('{self.title}', '{self.date_posted}')"
