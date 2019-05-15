import logging.config

import click
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restplus import Api
from config import Config
import status
import os

logging_conf_path = os.path.normpath(os.path.join(
    os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)

db = SQLAlchemy()
migrate = Migrate()
api = Api()

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'Access denied.'
login_manager.login_message_category = 'info'


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='')

    from app.bing import bp as bing_bp
    app.register_blueprint(bing_bp, url_prefix='/bing')

    from app.github import bp as github_bp
    app.register_blueprint(github_bp, url_prefix='/gitub')

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.api.v1 import bp as api_v1_bp
    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)

    from app.commands import init_admin_command
    app.cli.add_command(init_admin_command)

    log.info('>>>>> Starting development server <<<<<')

    return app


app = create_app()


@app.context_processor
def inject_user():
    from flask_login import current_user
    user = current_user
    return dict(user=user)


@app.errorhandler(400)
def bad_request(e):
    return render_template('error.html', code=status.HTTP_400_BAD_REQUEST), 400


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', code=status.HTTP_404_NOT_FOUND), 404


@app.errorhandler(500)
def internale_server_error(e):
    return render_template('error.html', code=status.HTTP_500_INTERNAL_SERVER_ERROR), 500
