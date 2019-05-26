import tests.helpers as helpers


def post(client, payload):
    return helpers.post_json(client, "/auth/login", payload)


def test_registered_user_logs_in(client):
    helpers.add_user(
        username="Test", email="test@test.org", password="password123"
    )
    response, data = post(
        client, {"email": "test@test.org", "password": "password123"}
    )

    helpers.assert_json_response(response, 200)
    helpers.assert_data(data, "success", "Successfully logged in")


def test_registered_user_logs_in_wrong_password(client):
    helpers.add_user(
        username="Test", email="test@test.org", password="password123"
    )
    response, data = post(
        client, {"email": "test@test.org", "password": "oh_noes"}
    )

    helpers.assert_json_response(response, 400)
    helpers.assert_data(data, "fail", "Check password")


def test_not_registered_user_logs_in(client):
    response, data = post(
        client, {"email": "test@test.org", "password": "password123"}
    )

    helpers.assert_json_response(response, 404)
    helpers.assert_data(data, "fail", "User doesn't exist")
