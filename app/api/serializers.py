from flask_restplus import fields
from app.api import api

bing = api.model('Bing', {
    'url': fields.String(required=True, description='The url of wallpaper'),
    'title': fields.String(required=True, description='The title of wallpaper'),
    'caption': fields.String(required=True, description='The caption of wallpaper'),
    'hsh': fields.String(readOnly=True, description='The unique identifier of a bing'),
    'description': fields.String(required=True, description='The description of wallpaper'),
    'pub_date': fields.DateTime
})

pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})

page_of_bings = api.inherit('Page of bings', pagination, {
    'items': fields.List(fields.Nested(bing))
})
