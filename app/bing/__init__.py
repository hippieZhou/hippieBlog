
from flask import Blueprint

bp = Blueprint('bing', __name__, template_folder="templates/bing")

from app.bing import views
