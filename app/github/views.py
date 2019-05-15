from flask import render_template, request
import json
import requests
from app.github import bp


@bp.route('/')
def index():
    req = requests.get(
        "https://raw.githubusercontent.com/xibang/github-rank-china/master/data/0.json")
    data = json.loads(req.text)
    print(data)
    return render_template('github/index.html', title='Github')
