from flask import (render_template, make_response, send_from_directory)
from . import bp


@bp.route('/')
def index():
    return render_template('main/index.html')


@bp.route('/about')
def about():
    return render_template('main/about.html', title='About')


@bp.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')


@bp.route('/sw.js')
def service_worker():
    response = make_response(send_from_directory('static', 'sw.js'))
    response.headers['Cache-Control'] = 'no-cache'
    return response
