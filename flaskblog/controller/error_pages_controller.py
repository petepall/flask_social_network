import flask.templating
from flask import Blueprint


errors = Blueprint("errors", __name__)


@errors.app_errorhandler(404)
def error_404(error):
    """Route function for handling 404 error pages
    """
    return flask.templating.render_template("errors/404.html.j2"), 404


@errors.app_errorhandler(403)
def error_403(error):
    """Route function for handling 403 error pages
    """
    return flask.templating.render_template("errors/403.html.j2"), 403


@errors.app_errorhandler(500)
def error_500(error):
    """Route function for handling 500 error pages
    """
    return flask.templating.render_template("errors/500.html.j2"), 500
