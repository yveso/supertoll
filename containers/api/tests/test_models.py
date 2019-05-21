import pytest
from sqlalchemy.exc import IntegrityError
from helpers import add_user


def test_user_just_add_one(client):
    user = add_user(username="Test", email="test@test.org")
    assert user.id is not None
    assert user.username == "Test"
    assert user.email == "test@test.org"
    assert user.active is True


def test_user_to_json(client):
    user = add_user(username="Test", email="test@test.org")

    assert isinstance(user.to_json(), dict)


def test_user_no_duplicate_username(client):
    with pytest.raises(IntegrityError):
        add_user(username="Test", email="test@test.org")
        add_user(username="Test", email="test2@test.org")


def test_user_no_duplicate_email(client):
    with pytest.raises(IntegrityError):
        add_user(username="Test", email="test@test.org")
        add_user(username="Test2", email="test@test.org")
