import os
from api import create_app, config


def test_TestingConfig():
    app = create_app()
    app.config.from_object(config.TestingConfig)

    assert app.config["TESTING"] is True
    assert app.config["SQLALCHEMY_DATABASE_URI"] == os.environ.get(
        "DATABASE_TEST_URL"
    )


def test_DevelopmentConfig():
    app = create_app()
    app.config.from_object(config.DevelopmentConfig)

    assert app.config["TESTING"] is False
    assert app.config["SQLALCHEMY_DATABASE_URI"] == os.environ.get(
        "DATABASE_URL"
    )


def test_ProductionConfig():
    app = create_app()
    app.config.from_object(config.ProductionConfig)

    assert app.config["TESTING"] is False
    assert app.config["SQLALCHEMY_DATABASE_URI"] == os.environ.get(
        "DATABASE_URL"
    )
