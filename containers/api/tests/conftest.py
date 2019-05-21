import pytest
from api import create_app, config, db


@pytest.fixture()
def client():
    app = create_app()
    app.config.from_object(config.TestingConfig)

    app.app_context().push()
    db.create_all()
    db.session.commit()

    yield app.test_client()

    db.session.remove()
    db.drop_all()
