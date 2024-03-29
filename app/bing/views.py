from flask import render_template, request
from datetime import date
from app import cache
from app.bing import bp


@bp.route('/')
def index():
    from app.models import Bing
    bings = Bing.query.order_by(Bing.pub_date.desc())

    first = bings.first()
    if first is None or first.pub_date.date() < date.today():
        from app.utils import bing_spider
        bing_spider.spider()

    bings = Bing.query.order_by(Bing.pub_date.desc())
    page = request.args.get('page', 1, type=int)
    others = bings.paginate(page, 10, False)

    return render_template('bing/index.html', others=others, title='Bing')


@bp.route('/detail/<hsh>', methods=['GET', 'POST'])
def detail(hsh):
    first = cache.get(hsh)
    if first is None:
        from app.models import Bing
        first = Bing.query.filter_by(hsh=hsh).first()
        cache.set(str(hsh), first, timeout=5*60)
    return render_template('bing/detail.html', first=first, title='Bing')
