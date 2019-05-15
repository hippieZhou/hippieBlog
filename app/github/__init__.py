
from flask import Blueprint

bp = Blueprint('github', __name__, template_folder="templates/github")

from app.github import views
