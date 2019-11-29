import flask
import flask_bcrypt
import flask_login
import flask_mail
import flask_sqlalchemy as flask_sqa

import flaskblog.config as flaskblog_cf

db = flask_sqa.SQLAlchemy()
bcrypt = flask_bcrypt.Bcrypt()
login_manager = flask_login.LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
mail = flask_mail.Mail()


def create_app(config_class=flaskblog_cf.Config):
    """Creates the app and initializes the config of the app

    Parameters
    ----------

    config_class : Object, optional

        Manage the app setup settings, by default Config
    """
    app = flask.Flask(__name__)
    app.config.from_object(flaskblog_cf.Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    import flaskblog.controller.user_controller as flaskblog_user_ctrl
    import flaskblog.controller.general_controller as flaskblog_general_ctrl
    import flaskblog.controller.posts_controller as flaskblog_post_ctrl
    import flaskblog.controller.error_pages_controller as flaskblog_error_ctrl

    app.register_blueprint(flaskblog_user_ctrl.users)
    app.register_blueprint(flaskblog_post_ctrl.posts)
    app.register_blueprint(flaskblog_general_ctrl.main)
    app.register_blueprint(flaskblog_error_ctrl.errors)

    return app
