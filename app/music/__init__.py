from flask import Blueprint

bp = Blueprint('music', __name__, template_folder="templates/music")

from . import views