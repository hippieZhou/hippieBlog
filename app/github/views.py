from flask import render_template, request
from app.github import bp


@bp.route('/')
def index():
    import requests
    req = requests.get(
        "https://raw.githubusercontent.com/xibang/github-rank-china/master/data/0.json")
    items = []
    if req.status_code == 200:
        import json
        from collections import namedtuple
        data = json.loads(req.text, object_hook=lambda d: namedtuple(
            'Rank', d.keys())(*d.values()))
        if data:
            page = 0
            count = 100
            total = data.total
            date = data.date
            items = data.list[page:count]
        return render_template('github/index.html', title='Github', items=items)

    # import os
    # file = os.path.join(os.path.dirname(__file__), '0.json')
    # print(file)
    # text = None
    # with open(file, encoding='utf-8') as f:
    #     text = f.read()
    # import json
    # from collections import namedtuple
    # data = json.loads(text, object_hook=lambda d: namedtuple(
    #     'Rank', d.keys())(*d.values()))
    # page = 0
    # count = 100

    # total = data.total
    # date = data.date
    # items = data.list[page:count]
    # print(items)
    # return render_template('github/index.html', title='Github', items=items)
