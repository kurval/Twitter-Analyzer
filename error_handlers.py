from flask import Blueprint, render_template, request

blueprint = Blueprint('error_handlers', __name__)

@blueprint.app_errorhandler(404)
def not_found(e):
    return render_template('error_login.html')