class Redprint():
    def __init__(self, name):
        self.name = name
        self.mound = []

    def route(self, rule, **options):
        def decoreate(f):
            self.mound.append((f, rule, options))
            return f

        return decoreate

    def register(self, bp, url_prfix=None):
        if url_prfix is None:
            url_prfix = '/' + self.name
        for f, rule, options in self.mound:
            endpoint = options.pop("endpoint", f.__name__)
            bp.add_url_rule(url_prfix + rule, endpoint, f, **options)


# usage：
# def create_blueprint_v1():
#     bp = Blueprint('v1', __name__)
#     bing.api.register(bp, url_prfix='/bing')
#     return bp