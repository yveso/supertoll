import json

from tests.helpers import add_user


def test_get(client):
    """Get all users"""
    add_user("Test", "test@test.com")
    add_user("Test2", "foo@bar.com")

    response = client.get("/users")
    data = json.loads(response.data.decode())

    assert response.status_code == 200
    assert "success" in data["status"]
    assert len(data["data"]["users"]) == 2


def test_get_id(client):
    """Get a single user"""
    user = add_user("Test", "test@test.com")

    response = client.get(f"/users/{user.id}")
    data = json.loads(response.data.decode())

    assert response.status_code == 200
    assert "success" in data["status"]
    assert "Test" in data["data"]["username"]
    assert "test@test.com" in data["data"]["email"]


def test_get_id_no_valid_id(client):
    """Get a single user, no valid id"""
    response = client.get("/users/not_a_id")
    data = json.loads(response.data.decode())

    assert response.status_code == 404
    assert "fail" in data["status"]
    assert "User does not exist" in data["message"]


def test_get_id_unknown_id(client):
    """Get a single user, unknown id"""
    response = client.get("/users/999999")
    data = json.loads(response.data.decode())

    assert response.status_code == 404
    assert "fail" in data["status"]
    assert "User does not exist" in data["message"]


def test_post(client):
    """Post a new user"""
    response = client.post(
        "/users",
        data=json.dumps(
            {
                "username": "John Doe",
                "email": "john@doe.org",
                "password": "password123",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 201
    assert "john@doe.org was added!" in data["message"]
    assert "success" in data["status"]


def test_post_empty_payload(client):
    """Post a new user with empty payload
    Error is thrown"""
    response = client.post(
        "/users", data=json.dumps({}), content_type="application/json"
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 400
    assert "Invalid payload" in data["message"]
    assert "fail" in data["status"]


def test_post_no_username(client):
    """Post a new user with no username in payload
    Error is thrown"""
    response = client.post(
        "/users",
        data=json.dumps({"email": "john@doe.org"}),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 400
    assert "Invalid payload" in data["message"]
    assert "fail" in data["status"]


def test_post_no_email(client):
    """Post a new user with no email in payload
    Error is thrown"""
    response = client.post(
        "/users",
        data=json.dumps({"username": "John Doe"}),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 400
    assert "Invalid payload" in data["message"]
    assert "fail" in data["status"]


def test_post_no_password(client):
    """Post a new user with no password in payload
    Error is thrown"""
    response = client.post(
        "/users",
        data=json.dumps({"username": "John Doe", "email": "john@doe.com"}),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 400
    assert "Invalid payload" in data["message"]
    assert "fail" in data["status"]


def test_post_email_twice(client):
    """Post same email twice
    Error is thrown"""
    client.post(
        "/users",
        data=json.dumps(
            {
                "username": "John Doe",
                "email": "john@doe.org",
                "password": "password123",
            }
        ),
        content_type="application/json",
    )
    response = client.post(
        "/users",
        data=json.dumps(
            {
                "username": "John Doe2",
                "email": "john@doe.org",
                "password": "password123",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 400
    assert "Email already exists." in data["message"]
    assert "fail" in data["status"]
