from flask import render_template
from app.main import bp

import status


@bp.app_errorhandler(400)
def bad_request(e):
    return render_template('error.html', code=status.HTTP_400_BAD_REQUEST), 400


@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('error.html', code=status.HTTP_404_NOT_FOUND), 404


@bp.app_errorhandler(500)
def internale_server_error(e):
    return render_template('error.html', code=status.HTTP_500_INTERNAL_SERVER_ERROR), 500
