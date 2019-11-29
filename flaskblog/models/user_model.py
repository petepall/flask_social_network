import flask
import flask_login
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

import flaskblog


@flaskblog.login_manager.user_loader
def load_user(user_id):
    """Load the current user's id

    Parameters
    ----------
    user_id : int

        ID of the current connected user
    """
    return User.query.get(int(user_id))


class User(flaskblog.db.Model, flask_login.UserMixin):
    """Class representing the User table in the database

    Parameters
    ----------
    db : Database object

        Represents the database model base class

    UserMixin : Flask user management object

        Enables Flask user management functions
    """

    id = flaskblog.db.Column(flaskblog.db.Integer, primary_key=True)
    username = flaskblog.db.Column(
        flaskblog.db.String(20), unique=True, nullable=False
    )
    email = flaskblog.db.Column(
        flaskblog.db.String(120), unique=True, nullable=False
    )
    image_file = flaskblog.db.Column(
        flaskblog.db.String(20), nullable=False, default="default.jpg"
    )
    password = flaskblog.db.Column(flaskblog.db.String(60), nullable=False)
    posts = flaskblog.db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        """String representation for the User
        """
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    def get_reset_token(self, expires_seconds=1800):
        """Get a token for user password reset, that is send by email

        Parameters
        ----------
        expires_seconds : int, optional

            delay in seconds after which the token expires, by default 1800
        """
        s = Serializer(flask.current_app.config["SECRET_KEY"], expires_seconds)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        """Verify if a given token is valid

        Parameters
        ----------
        token : token

            Token to verify
        """
        s = Serializer(flask.current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:  # noqa
            return None
        return User.query.get(user_id)
