import os
from flask import Flask


def create_app():
    app = Flask(__name__)
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    from api.sanity import bp as sanity_bp

    app.register_blueprint(sanity_bp)

    return app
