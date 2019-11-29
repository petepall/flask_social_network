from datetime import datetime

import flaskblog


class Post(flaskblog.db.Model):
    """Class representing the Post table in the database

    Parameters
    ----------
    db : database object

        represents the database object.
    """

    id = flaskblog.db.Column(flaskblog.db.Integer, primary_key=True)
    title = flaskblog.db.Column(flaskblog.db.String(100), nullable=False)
    date_posted = flaskblog.db.Column(
        flaskblog.db.DateTime, nullable=False, default=datetime.utcnow
    )
    content = flaskblog.db.Column(flaskblog.db.Text, nullable=False)
    user_id = flaskblog.db.Column(
        flaskblog.db.Integer,
        flaskblog.db.ForeignKey("user.id"),
        nullable=False,
    )

    def __repr__(self):
        """String representation of the post object
        """
        return f"Post('{self.title}', '{self.date_posted}')"
