from flask import Flask


def create_app():
    app = Flask(__name__)

    from api.sanity import bp as sanity_bp
    app.register_blueprint(sanity_bp)

    return app
