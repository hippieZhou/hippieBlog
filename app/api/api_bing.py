
from flask import jsonify, request
from datetime import datetime
import random
import status
from . import bp


@bp.route('/bing', methods=['GET'])
def bing():
    headers = dict(request.headers)
    token = headers.setdefault('Authorization', None)
    content_type = headers.setdefault('Content-Type', None)
    if token != 'dev hippiezhou.fun' or content_type is None or content_type != "application/json; charset=utf-8":
        return jsonify(code=status.HTTP_403_FORBIDDEN, msg='not allowed.')

    from app.models import Bing
    fullstartdate = request.args.get('day')
    if fullstartdate:
        try:
            seed = datetime.strptime(fullstartdate, '%Y%m%d')
            seed_str = '{0}%'.format(seed.strftime('%Y-%m-%d'))
            first = Bing.query.filter(Bing.datetime.like(seed_str)).first()
            if first:
                return jsonify(code=status.HTTP_200_OK, data=first.get_json())
            else:
                return jsonify(code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return jsonify(code=status.HTTP_400_BAD_REQUEST, msg='day is error.')
    else:
        bings = Bing.query.all()
        return jsonify(code=status.HTTP_200_OK,
                       data=random.choice(bings).get_json())


@bp.route('/bings', methods=['GET'])
def bings():
    headers = dict(request.headers)
    token = headers.setdefault('Authorization', None)
    content_type = headers.setdefault('Content-Type', None)
    if token != 'dev hippiezhou.fun' or content_type is None or content_type != "application/json; charset=utf-8":
        return jsonify(code=status.HTTP_403_FORBIDDEN, msg='not allowed.')

    page = request.args.get('page', type=int)
    per_page = request.args.get('per_page', type=int)

    if page is None or per_page is None:
        return jsonify(code=status.HTTP_400_BAD_REQUEST, msg='arguements is error.')
    else:
        from app.models import Bing
        val = Bing.query.order_by(
            Bing.datetime.desc()).paginate(page, per_page, False)
        return jsonify(code=status.HTTP_200_OK, data=[p.get_json() for p in val.items])
