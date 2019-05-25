import json

from tests.helpers import add_user


def post(client, payload):
    response = client.post(
        "/auth/login",
        data=json.dumps(payload),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())
    return response, data


def assert_response(response, expected_status_code):
    assert response.content_type == "application/json"
    assert response.status_code == expected_status_code


def assert_data(data, expected_status, expoected_message):
    assert data["status"] == expected_status
    assert data["message"] == expoected_message


def test_post_registered_user_logs_in(client):
    add_user(username="Test", email="test@test.org", password="password123")
    response, data = post(
        client, {"email": "test@test.org", "password": "password123"}
    )

    assert_response(response, 200)
    assert_data(data, "success", "Successfully logged in")


def test_post_registered_user_logs_in_wrong_password(client):
    add_user(username="Test", email="test@test.org", password="password123")
    response, data = post(
        client, {"email": "test@test.org", "password": "oh_noes"}
    )

    assert_response(response, 400)
    assert_data(data, "fail", "Check password")


def test_post_not_registered_user_logs_in(client):
    response, data = post(
        client, {"email": "test@test.org", "password": "password123"}
    )

    assert_response(response, 404)
    assert_data(data, "fail", "User doesn't exist")
