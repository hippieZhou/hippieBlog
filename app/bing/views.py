from flask import render_template, request
from . import bp
from .bing_api import restore_bing_wallpapers
from datetime import date


@bp.route('/')
def index():
    from app.models import bing
    bings = bing.query.order_by(bing.datetime.desc())

    first_time = bings.first().datetime.date()
    today = date.today()
    print(today, first_time)
    if(first_time < today):
        print('need to request new bing data')
        restore_bing_wallpapers()

    bings = bing.query.order_by(bing.datetime.desc())
    page = request.args.get('page', 1, type=int)
    others = bings.paginate(page, 10, False)

    return render_template('bing/index.html', others=others)


@bp.route('/detail/<hsh>', methods=['GET', 'POST'])
def detail(hsh):
    from app.models import bing
    first = bing.query.filter_by(hsh=hsh).first_or_404()
    return render_template('bing/detail.html', first=first)
