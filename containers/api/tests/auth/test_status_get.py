import tests.helpers as helpers


def get(client, headers):
    return helpers.get_with_headers(client, "/auth/status", headers)


def test_valid(client):
    username, email, password = "Test Me", "me@test.com", "password12345"
    token = helpers.log_user_in_and_get_token(
        client, username, email, password
    )

    response, data = get(client, {"Authorization": f"Bearer {token}"})

    helpers.assert_json_response(response, 200)
    helpers.assert_data(data, "success", "Success")
    inner_data = data["data"]
    assert inner_data is not None
    assert inner_data["username"] == username
    assert inner_data["email"] == email
    assert inner_data["active"] is True


def test_invalid(client):
    response, data = get(client, {"Authorization": "Bearer invalid"})

    helpers.assert_json_response(response, 401)
    helpers.assert_data(data, "fail", "Invalid token")
