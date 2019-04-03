from flask import Flask, render_template
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.bing import bp as bing_bp
    app.register_blueprint(bing_bp, url_prefix='/bing')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app


app = create_app()


@app.errorhandler(400)
def bad_request(e):
    return render_template('errors/400.html'), 400


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internale_server_error(e):
    return render_template('errors/500.html'), 500
