import json
from api import db
from api.models import User


def add_user(username, email, password="password123"):
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user


def post_json(client, route, payload):
    response = client.post(
        route, data=json.dumps(payload), content_type="application/json"
    )
    data = json.loads(response.data.decode())
    return response, data


def get_with_headers(client, route, headers):
    response = client.get(route, headers=headers)
    data = json.loads(response.data.decode())
    return response, data


def assert_json_response(response, expected_status_code):
    assert response.content_type == "application/json"
    assert response.status_code == expected_status_code


def assert_data(data, expected_status, expected_message):
    assert data["status"] == expected_status
    assert data["message"] == expected_message


def log_user_in_and_get_token(
    client, username="test", email="test@test.org", password="abc123"
):
    add_user(username, email, password)
    _, login_data = post_json(
        client, "/auth/login", {"email": email, "password": password}
    )
    token = login_data["auth_token"]
    return token
