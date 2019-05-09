from app.utils.redprint import Redprint

from flask import jsonify, request
from datetime import datetime
import random
import status


api = Redprint('bing')


def auth():
    headers = dict(request.headers)
    token = headers.setdefault('Authorization', None)
    content_type = headers.setdefault('Content-Type', None)
    return token == 'dev hippiezhou.fun' and content_type == "application/json; charset=utf-8"


@api.route('/today', methods=['GET'])
def today():
    # ok = auth()
    # if ok == False:
    #     return jsonify(code=status.HTTP_403_FORBIDDEN, msg='not allowed.')
    from app.models import Bing
    today = Bing.query.order_by(Bing.datetime.desc()).first_or_404()
    return jsonify(
        code=status.HTTP_200_OK,
        data=today.get_json()
    )


@api.route('/oneday', methods=['GET'])
def oneday():

    ok = auth()
    if ok == False:
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


@api.route('/all', methods=['GET'])
def all():

    ok = auth()
    if ok == False:
        return jsonify(code=status.HTTP_403_FORBIDDEN, msg='not allowed.')

    page = request.args.get('page', type=int)
    per_page = request.args.get('per_page', type=int)

    if page and per_page:
        from app.models import Bing
        val = Bing.query.order_by(
            Bing.datetime.desc()).paginate(page, per_page, False)
        return jsonify(code=status.HTTP_200_OK, data=[p.get_json() for p in val.items])
    else:
        return jsonify(code=status.HTTP_400_BAD_REQUEST, msg='arguements is error.')
