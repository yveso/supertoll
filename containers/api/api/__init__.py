import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
toolbar = DebugToolbarExtension()
cors = CORS()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    db.init_app(app)
    toolbar.init_app(app)
    cors.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    from . import models  # noqa

    @app.route("/")
    def index():
        users = models.User.query.all()
        return render_template("index.html", users=users)

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

    @app.cli.command()
    def seed_db():
        db.session.add(models.User(username="Test", email="test@test.com"))
        db.session.add(models.User(username="Foo Bar", email="foo@bar.com"))
        db.session.commit()

    return app
