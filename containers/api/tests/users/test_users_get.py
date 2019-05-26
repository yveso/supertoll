import json

import tests.helpers as helpers


def test_all_users(client):
    helpers.add_user("Test", "test@test.com")
    helpers.add_user("Test2", "foo@bar.com")

    response = client.get("/users")
    data = json.loads(response.data.decode())

    helpers.assert_json_response(response, 200)
    assert "success" in data["status"]
    assert len(data["data"]["users"]) == 2


def test_single_id(client):
    user = helpers.add_user("Test", "test@test.com")

    response = client.get(f"/users/{user.id}")
    data = json.loads(response.data.decode())

    helpers.assert_json_response(response, 200)
    assert "success" in data["status"]
    assert "Test" in data["data"]["username"]
    assert "test@test.com" in data["data"]["email"]


def test_no_valid_id(client):
    response = client.get("/users/not_a_id")
    data = json.loads(response.data.decode())

    helpers.assert_json_response(response, 404)
    helpers.assert_data(data, "fail", "User does not exist.")


def test_unknown_id(client):
    response = client.get("/users/999999")
    data = json.loads(response.data.decode())

    helpers.assert_json_response(response, 404)
    helpers.assert_data(data, "fail", "User does not exist.")
