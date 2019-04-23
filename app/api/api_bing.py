
from flask import jsonify, request
from datetime import datetime
import random
import status
from . import bp


@bp.route('/bing', methods=['GET'])
def bing():
    headers = dict(request.headers)
    token = headers.setdefault('Auth-Token', None)
    content_type = headers.setdefault('Content-Type', None)
    if token != 'hippiezhou.fun' or content_type is None or content_type != "application/json":
        return jsonify(code=status.HTTP_403_FORBIDDEN)

    from app.models import Bing
    fullstartdate = request.args.get('day')
    try:
        if fullstartdate:
            seed = datetime.strptime(fullstartdate, '%Y%m%d')
            start = datetime(seed.year, seed.month, seed.day, 0, 0, 0)
            end = datetime(seed.year, seed.month, seed.day, 23, 59, 59)
            print(start, end)
            first = Bing.query.filter(
                Bing.datetime >= start, Bing.datetime <= end).first()
            if first:
                return jsonify(code=status.HTTP_200_OK, data=first.get_json())
            else:
                return jsonify(code=status.HTTP_404_NOT_FOUND)
        else:
            bings = Bing.query.all()
            return jsonify(code=status.HTTP_200_OK,
                           data=random.choice(bings).get_json())
    except Exception as e:
        print(e)
        return jsonify(code=status.HTTP_500_INTERNAL_SERVER_ERROR)
