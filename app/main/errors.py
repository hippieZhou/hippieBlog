from flask import render_template
from . import bp


@bp.errorhandler(400)
def bad_request(e):
    return render_template('errors/400.html'), 400


@bp.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@bp.errorhandler(500)
def internale_server_error(e):
    return render_template('errors/500.html'), 500
