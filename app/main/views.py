from flask import (render_template, make_response, send_from_directory)
from . import bp


@bp.route('/')
@bp.route('/index')
def index():
    from flask import request
    trusted_proxies = {'127.0.0.1'}
    route = request.access_route + [request.remote_addr]
    remote_addr = next((addr for addr in reversed(route)
                        if addr not in trusted_proxies), request.remote_addr)
    # print(remote_addr)
    from app.models import Visitor
    has = Visitor.query.filter(Visitor.addr == remote_addr).first()
    if not has:
        from app import db
        visitor = Visitor(addr=remote_addr)
        db.session.add(visitor)
        db.session.commit()

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
