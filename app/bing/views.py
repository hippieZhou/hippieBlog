from flask import render_template, request
from . import bp


@bp.route('/')
def index():
    from app.models import bing
    bings = bing.query.order_by(bing.datetime.desc())
    first = bings[0]

    page = request.args.get('page', 1, type=int)
    others = bings.paginate(page, 9, False)

    return render_template('bing/index.html', first=first, others=others)


@bp.route('/detail/<hsh>', methods=['GET', 'POST'])
def detail(hsh):
    from app.models import bing
    first = bing.query.filter_by(hsh=hsh).first_or_404()
    return render_template('bing/detail.html', first=first)
