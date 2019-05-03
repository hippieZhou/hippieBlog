from flask import render_template, request
from . import bp
from .bing_spider import restore_bing_wallpapers
from datetime import date


@bp.route('/')
def index():
    from app.models import Bing
    bings = Bing.query.order_by(Bing.datetime.desc())

    first_time = bings.first().datetime.date()
    today = date.today()
    print(today, first_time)
    if(first_time < today):
        restore_bing_wallpapers()

    bings = Bing.query.order_by(Bing.datetime.desc())
    page = request.args.get('page', 1, type=int)
    others = bings.paginate(page, 10, False)

    return render_template('bing/index.html', others=others,title='Bing')


@bp.route('/detail/<hsh>', methods=['GET', 'POST'])
def detail(hsh):
    from app.models import Bing
    first = Bing.query.filter_by(hsh=hsh).first_or_404()
    return render_template('bing/detail.html', first=first,title='Bing')
