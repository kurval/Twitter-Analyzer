from flask import Blueprint, render_template, request

blueprint = Blueprint('error_handlers', __name__)

@blueprint.app_errorhandler(400)
def bad_request(e):
    return render_template('error_bad_request.html')

@blueprint.app_errorhandler(401)
def forbidden(e):
    return render_template('error_login.html')

@blueprint.app_errorhandler(404)
def not_found(e):
    return render_template('error_not_found.html', error=e)
