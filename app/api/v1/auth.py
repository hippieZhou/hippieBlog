from app.api.v1 import api
from flask_restplus import Resource
import status

ns = api.namespace('authorizations', description='hello world')


@api.route('/authorizations/')
class Authorized(Resource):
    def get(self):
        return {'code': status.HTTP_200_OK}


@api.route('/without-authorization/')
class WithoutAuthorization(Resource):
    def get(self):
        return {'code': status.HTTP_200_OK}

    def post(self):
        return {'code': status.HTTP_200_OK}
