import pytest
from api import create_app, config, db


@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.config.from_object(config.TestingConfig)

    app.app_context().push()
    db.create_all()
    db.session.commit()

    yield app

    db.session.remove()
    db.drop_all()
