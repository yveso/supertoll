import pytest
from api import create_app, config


@pytest.fixture
def app():
    app = create_app()
    app.config.from_object(config.TestingConfig)
    return app
