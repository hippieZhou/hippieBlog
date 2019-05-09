from flask import Blueprint
from app.api.v1 import bing


def create_blueprint_v1():
    bp = Blueprint('v1', __name__)
    bing.api.register(bp, url_prfix='/bing')
    return bp
