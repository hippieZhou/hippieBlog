
from flask import jsonify, request
import random
import status
from . import bp


@bp.route('/bing', methods=['GET'])
def bing():
    day = request.args.get('day')
    response = None
    from app.models import Bing
    bings = Bing.query.all()
    if day:
        response = {
            'status_code': status.HTTP_200_OK,
            'data': 'helloworld',
            'day': day
        }
    else:
        response = {
            'status_code ': status.HTTP_200_OK,
            'bing': random.choice(bings).title,
            'accept': request.headers['accept']
        }
    return jsonify(response)
