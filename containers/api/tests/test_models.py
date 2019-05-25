import pytest
from sqlalchemy.exc import IntegrityError

from api.models import User
from helpers import add_user


def test_user_just_add_one(client):
    user = add_user(username="Test", email="test@test.org")
    assert user.id is not None
    assert user.username == "Test"
    assert user.email == "test@test.org"
    assert user.active is True
    assert user.password_hash is not None


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


def test_user_password_hashes_are_randon(client):
    user1 = add_user(
        username="Test 1", email="test1@test.org", password="this_is_equal"
    )
    user2 = add_user(
        username="Test 2", email="test2@test.org", password="this_is_equal"
    )
    assert user1.password_hash != user2.password_hash


def test_user_encode_auth_token(client):
    user = add_user(
        username="Test", email="test@test.org", password="password123"
    )
    auth_token = user.encode_auth_token()
    assert isinstance(auth_token, bytes)


def test_user_decode_auth_token(client):
    user = add_user(
        username="Test", email="test@test.org", password="password123"
    )
    auth_token = user.encode_auth_token()
    assert User.decode_auth_token(auth_token) == user.id
