from app.models import Bing
from flask_restplus import Resource
from datetime import datetime
from app.api import api
from app.api.parsers import pagination_arguments
from app.api.serializers import page_of_bings


ns = api.namespace('Bing', description='The WebAPI of Bing Wallpapers.')


@ns.route('/')
@ns.route('/<int:year>/')
@ns.route('/<int:year>/<int:month>/')
@ns.route('/<int:year>/<int:month>/<int:day>/')
class BingList(Resource):
    @api.expect(pagination_arguments, validate=True)
    @api.marshal_with(page_of_bings)
    def get(self, year=None, month=None, day=None):
        from flask import request
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        start_year = year if year else 2000
        end_year = year if year else datetime.now().year
        start_month = month if month else 1
        end_month = month if month else 12
        start_day = day if day else 1
        end_day = day + 1 if day else 31
        start_date = '{0:04d}-{1:02d}-{2:02d}'.format(
            start_year, start_month, start_day)
        end_date = '{0:04d}-{1:02d}-{2:02d}'.format(
            end_year, end_month, end_day)
        bings_query = Bing.query.filter(
            Bing.pub_date >= start_date).filter(Bing.pub_date <= end_date).order_by(Bing.pub_date.desc())
        bings_page = bings_query.paginate(page, per_page, error_out=False)
        return bings_page
