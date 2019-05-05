import click
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import status

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='')

    from app.bing import bp as bing_bp
    app.register_blueprint(bing_bp, url_prefix='/bing')

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    db.init_app(app)

    migrate.init_app(app, db)

    return app


app = create_app()


@app.errorhandler(400)
def bad_request(e):
    return render_template('error.html', code=status.HTTP_400_BAD_REQUEST), 400


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', code=status.HTTP_404_NOT_FOUND), 404


@app.errorhandler(500)
def internale_server_error(e):
    return render_template('error.html', code=status.HTTP_500_INTERNAL_SERVER_ERROR), 500
