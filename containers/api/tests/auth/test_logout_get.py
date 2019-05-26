from flask import current_app

import tests.helpers as helpers


def get(client, headers):
    return helpers.get_with_headers(client, "/auth/logout", headers)


def test_valid_logout(client):
    token = helpers.log_user_in_and_get_token(client)

    response, data = get(client, {"Authorization": f"Bearer {token}"})

    helpers.assert_json_response(response, 200)
    helpers.assert_data(data, "success", "Successfully logged out")


def test_invalid_logout(client):
    response, data = get(client, {"Authorization": f"Bearer invalid"})

    helpers.assert_json_response(response, 401)
    helpers.assert_data(data, "fail", "Invalid token")


def test_missing_header(client):
    response, data = get(client, None)

    helpers.assert_json_response(response, 403)
    helpers.assert_data(data, "fail", "Missing header")


def test_expired_token(client):
    current_app.config["TOKEN_EXPIRATION_SECONDS"] = -1
    token = helpers.log_user_in_and_get_token(client)

    response, data = get(client, {"Authorization": f"Bearer {token}"})

    helpers.assert_json_response(response, 401)
    helpers.assert_data(data, "fail", "Signature expired")
