from app.models import Bing
from flask import request
from flask_restplus import Namespace, Resource, fields, reqparse
from datetime import datetime
import status

ns = Namespace('bing', description='The APIs of Bing Wallpapers')

# models

bing = ns.model('Bing', {
    'hsh': fields.String(required=True, description='The unique identifier of a bing'),
    'url': fields.String(readOnly=True, description='The url of wallpaper'),
    'title': fields.String(readOnly=True, description='The title of wallpaper'),
    'caption': fields.String(readOnly=True, description='The caption of wallpaper'),
    'description': fields.String(readOnly=True, description='The description of wallpaper'),
    'pub_date': fields.DateTime
})

pagination = ns.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})

page_of_bings = ns.inherit('Page of bings', pagination, {
    'items': fields.List(fields.Nested(bing))
})


# arguments

pagination_arguments = reqparse.RequestParser()
pagination_arguments.add_argument('page',
                                  type=int, required=False, default=1, help='Page number')
pagination_arguments.add_argument('per_page',
                                  type=int, required=False, choices=[2, 10, 20, 30, 40, 50],
                                  default=10, help='Results per page {error_msg}')


@ns.route('/')
@ns.route('/<int:year>/')
@ns.route('/<int:year>/<int:month>/')
@ns.route('/<int:year>/<int:month>/<int:day>/')
class BingList(Resource):
    @ns.expect(pagination_arguments, validate=True)
    @ns.marshal_with(page_of_bings)
    @ns.doc(responses={
        status.HTTP_200_OK: 'HTTP_200_OK',
        status.HTTP_400_BAD_REQUEST: 'HTTP_400_BAD_REQUEST',
        status.HTTP_401_UNAUTHORIZED: 'HTTP_401_UNAUTHORIZED',
        status.HTTP_404_NOT_FOUND: 'HTTP_404_NOT_FOUND',
        status.HTTP_500_INTERNAL_SERVER_ERROR: 'HTTP_500_INTERNAL_SERVER_ERROR'
    })
    def get(self, year=None, month=None, day=None):
        args = pagination_arguments.parse_args(request)

        ip = request.remote_addr
        from app.models import Visitor
        has = Visitor.query.filter(Visitor.addr == ip).first()
        from hashlib import md5
        h = md5()
        h.update(ip.encode(encoding='utf-8'))

        x_api_key = request.headers.get('X-API-KEY', None)
        if has and x_api_key == h.hexdigest():
            page = args.get('page', 1)
            per_page = args.get('per_page', 10)

            start_year = year if year else datetime.utcnow().year
            end_year = year if year else datetime.utcnow().year
            start_month = month if month else 1
            end_month = month if month else 12
            start_day = day if day else 1
            end_day = day+1 if day else 31
            start_date = '{0:04d}-{1:02d}-{2:02d}'.format(
                start_year, start_month, start_day)
            end_date = '{0:04d}-{1:02d}-{2:02d}'.format(
                end_year, end_month, end_day)

            bings_query = Bing.query.filter(
                Bing.pub_date >= start_date).filter(Bing.pub_date <= end_date).order_by(Bing.pub_date.desc())
            bings_page = bings_query.paginate(page, per_page, error_out=False)

            return bings_page
        else:
            return {'code': status.HTTP_401_UNAUTHORIZED}
