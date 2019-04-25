import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    db.init_app(app)

    from . import models  # noqa

    from api.sanity import bp as sanity_bp
    from api.users import bp as users_bp

    app.register_blueprint(sanity_bp)
    app.register_blueprint(users_bp)

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    @app.cli.command()
    def recreate_db():
        db.drop_all()
        db.create_all()
        db.session.commit()

    return app
