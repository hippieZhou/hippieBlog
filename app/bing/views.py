from flask import render_template
from . import bp

@bp.route('/')
def index():
    return render_template('bing/index.html')

@bp.route('/detail')
def detail():
    return render_template('bing/detail.html')