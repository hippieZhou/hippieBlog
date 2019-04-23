from flask import render_template
from music_dl.extractors import qq
from . import bp


@bp.route('/')
def index():
    # https://github.com/0xHJK/music-dl
    return render_template('music/index.html', title='Music')
