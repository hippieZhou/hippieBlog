from flask import Blueprint
from flask_restplus import Api, Resource
import status

# https://github.com/guomaoqiu/flask-restplus-jwt-auth
# https://medium.freecodecamp.org/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563?gi=a5d34ade4e54
# authorizations = {
#     'apikey': {
#         'type': 'apiKey',
#         'in': 'header',
#         'name': 'X-API-KEY'
#     }
# }

bp = Blueprint('api', __name__, template_folder='templates')
api = Api(bp,
          version='1.0',
          title='hippieZhou - SwaggerUI',
          contact="Author",
          contact_email='hippiezhou@outlook.com',
          description='Main APIs')


from .auth import ns as auth_namespace
api.add_namespace(auth_namespace)

from .bings import ns as bings_namespace
api.add_namespace(bings_namespace)
