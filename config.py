import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    EXPLAIN_TEMPLATE_LOADING = False
    DEBUG = True

    SECRET_KEY = os.environ.get('SECRET_KEY') or "you will never known it."

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
        'SQLALCHEMY_TRACK_MODIFICATIONS') or True
