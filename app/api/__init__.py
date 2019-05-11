from flask import Blueprint
from flask_restplus import Api, Resource
import status

bp = Blueprint('api', __name__)
api = Api(bp,
          version='1.0',
          title='hippieZhou - SwaggerUI',
          description='Main APIs')

ns = api.namespace(name='Home', description='The Test API')

@ns.route('/')
class HelloWorld(Resource):
    def get(self):
        return {
            'status': status.HTTP_200_OK,
            'msg': 'you get a request.'
        }

    def post(self):
        return {
            'status': status.HTTP_200_OK,
            'msg': 'you post a request.'
        }

from app.api.v1.bings import ns as bings_namespace
api.add_namespace(bings_namespace)