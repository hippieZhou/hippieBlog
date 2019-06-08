from flask import Flask
from werkzeug.contrib.cache import SimpleCache
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restplus import Api
from config import Config

from app.logger import Logger
log = Logger('all.log', level='debug')


cache = SimpleCache()
db = SQLAlchemy()
migrate = Migrate()
api = Api()


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'access denied.'
login_manager.login_message_category = 'info'


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='')

    from app.bing import bp as bing_bp
    app.register_blueprint(bing_bp, url_prefix='/bing')

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.api.v1 import bp as api_v1_bp
    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)

    from app.cmds import init_admin_command
    app.cli.add_command(init_admin_command)

    log.logger.info('>>>>> Starting development server <<<<<')

    return app
