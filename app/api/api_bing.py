
from flask import jsonify, request
import random
import status
from . import bp


@bp.route('/bing', methods=['GET'])
def bing():
    headers = dict(request.headers)
    token = headers.setdefault('Auth-Token', None)
    content_type = headers.setdefault('Content-Type', None)
    if token is None:
        return jsonify(code=status.HTTP_403_FORBIDDEN)
    if content_type is None or content_type != "application/json":
        return jsonify(code=status.HTTP_403_FORBIDDEN)
    else:
        day = request.args.get('day')
        from app.models import Bing
        bings = Bing.query.all()
        if day:
            return jsonify(code=status.HTTP_200_OK, msg='comming soon.')
        return jsonify(code=status.HTTP_200_OK,
                       data=random.choice(bings).get_json())
