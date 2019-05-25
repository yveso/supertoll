import json

from tests.helpers import add_user


def test_post_all_is_good(client):
    response = client.post(
        "/auth/register",
        data=json.dumps(
            {
                "username": "Test",
                "email": "test@test.org",
                "password": "password123",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 201
    assert response.content_type == "application/json"
    assert data["status"] == "success"
    assert data["message"] == "Successfully registered"
    assert data["auth_token"]


def test_post_username_already_exists(client):
    add_user(username="Test", email="doesnt@matter.com", password="123")
    response = client.post(
        "/auth/register",
        data=json.dumps(
            {
                "username": "Test",
                "email": "test@test.org",
                "password": "password123",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 400
    assert data["status"] == "fail"
    assert data["message"] == "User already exists"


def test_post_email_already_exists(client):
    add_user(username="Who ever", email="already@exists.com", password="123")
    response = client.post(
        "/auth/register",
        data=json.dumps(
            {
                "username": "Test",
                "email": "already@exists.com",
                "password": "password123",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 400
    assert data["status"] == "fail"
    assert data["message"] == "User already exists"


def test_post_empty_payload(client):
    response = client.post(
        "/auth/register", data=json.dumps({}), content_type="application/json"
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 400
    assert data["status"] == "fail"
    assert data["message"] == "Invalid payload"


def test_post_no_username_in_payload(client):
    response = client.post(
        "/auth/register",
        data=json.dumps({"email": "test@test.org", "password": "password123"}),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 400
    assert data["status"] == "fail"
    assert data["message"] == "Invalid payload"


def test_post_no_email_in_payload(client):
    response = client.post(
        "/auth/register",
        data=json.dumps({"username": "Test", "password": "password123"}),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 400
    assert data["status"] == "fail"
    assert data["message"] == "Invalid payload"


def test_post_no_password_in_payload(client):
    response = client.post(
        "/auth/register",
        data=json.dumps({"username": "Test", "email": "test@test.org"}),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 400
    assert data["status"] == "fail"
    assert data["message"] == "Invalid payload"
