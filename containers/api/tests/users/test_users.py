import json

from api import db
from api.models import User


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


def test_users_get(app):
    """Get all users"""
    client = app.test_client()

    add_user("Test", "test@test.com")
    add_user("Test2", "foo@bar.com")

    response = client.get("/users")
    data = json.loads(response.data.decode())

    assert response.status_code == 200
    assert "success" in data["status"]
    assert len(data["data"]["users"]) == 2


def test_users_get_id(app):
    """Get a single user"""
    client = app.test_client()

    user = add_user("Test", "test@test.com")

    response = client.get(f"/users/{user.id}")
    data = json.loads(response.data.decode())

    assert response.status_code == 200
    assert "success" in data["status"]
    assert "Test" in data["data"]["username"]
    assert "test@test.com" in data["data"]["email"]


def test_users_get_id_no_valid_id(app):
    """Get a single user, no valid id"""
    client = app.test_client()

    response = client.get("/users/not_a_id")
    data = json.loads(response.data.decode())

    assert response.status_code == 404
    assert "fail" in data["status"]
    assert "User does not exist" in data["message"]


def test_users_get_id_unknown_id(app):
    """Get a single user, unknown id"""
    client = app.test_client()

    response = client.get("/users/999999")
    data = json.loads(response.data.decode())

    assert response.status_code == 404
    assert "fail" in data["status"]
    assert "User does not exist" in data["message"]


def test_users_post(app):
    """Post a new user"""
    client = app.test_client()

    response = client.post(
        "/users",
        data=json.dumps({"username": "John Doe", "email": "john@doe.org"}),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 201
    assert "john@doe.org was added!" in data["message"]
    assert "success" in data["status"]


def test_users_post_empty_payload(app):
    """Post a new user with empty payload
    Error is thrown"""
    client = app.test_client()

    response = client.post(
        "/users", data=json.dumps({}), content_type="application/json"
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 400
    assert "Invalid payload" in data["message"]
    assert "fail" in data["status"]


def test_users_post_no_username(app):
    """Post a new user with no username in payload
    Error is thrown"""
    client = app.test_client()

    response = client.post(
        "/users",
        data=json.dumps({"email": "john@doe.org"}),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 400
    assert "Invalid payload" in data["message"]
    assert "fail" in data["status"]


def test_users_post_no_email(app):
    """Post a new user with no email in payload
    Error is thrown"""
    client = app.test_client()

    response = client.post(
        "/users",
        data=json.dumps({"username": "John Doe"}),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 400
    assert "Invalid payload" in data["message"]
    assert "fail" in data["status"]


def test_users_post_email_twice(app):
    """Post same email twice
    Error is thrown"""
    client = app.test_client()

    client.post(
        "/users",
        data=json.dumps({"username": "John Doe", "email": "john@doe.org"}),
        content_type="application/json",
    )
    response = client.post(
        "/users",
        data=json.dumps({"username": "John Doe2", "email": "john@doe.org"}),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 400
    assert "Email already exists." in data["message"]
    assert "fail" in data["status"]
