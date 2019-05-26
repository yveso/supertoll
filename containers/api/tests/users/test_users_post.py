import tests.helpers as helpers


def post(client, payload):
    return helpers.post_json(client, "/users", payload)


def test_everything_ok(client):
    response, data = post(
        client,
        {
            "username": "John Doe",
            "email": "john@doe.org",
            "password": "password123",
        },
    )

    helpers.assert_json_response(response, 201)
    helpers.assert_data(data, "success", "john@doe.org was added!")


def test_empty_payload(client):
    response, data = post(client, {})

    helpers.assert_json_response(response, 400)
    helpers.assert_data(data, "fail", "Invalid payload")


def test_no_username(client):
    response, data = post(client, {"email": "john@doe.org", "password": "123"})

    helpers.assert_json_response(response, 400)
    helpers.assert_data(data, "fail", "Invalid payload")


def test_no_email(client):
    response, data = post(client, {"username": "John Doe", "password": "123"})

    helpers.assert_json_response(response, 400)
    helpers.assert_data(data, "fail", "Invalid payload")


def test_no_password(client):
    response, data = post(
        client, {"username": "John Doe", "email": "john@doe.com"}
    )

    helpers.assert_json_response(response, 400)
    helpers.assert_data(data, "fail", "Invalid payload")


def test_email_twice(client):
    post(
        client,
        {"username": "John Doe", "email": "john@doe.com", "password": "123"},
    )
    response, data = post(
        client,
        {"username": "John Doe 2", "email": "john@doe.com", "password": "456"},
    )

    helpers.assert_json_response(response, 400)
    helpers.assert_data(data, "fail", "Email already exists.")
