from flask import Flask
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.bing import bp as bing_bp
    app.register_blueprint(bing_bp, url_prefix='/bing')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/')
    
    return app
