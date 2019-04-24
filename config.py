import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    EXPLAIN_TEMPLATE_LOADING = False
    DEBUG = True

    SECRET_KEY = os.environ.get('SECRET_KEY') or "{C3D6134D-2552-4F6F-A03A-9CCA42472F76}"

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
        'SQLALCHEMY_TRACK_MODIFICATIONS') or True
