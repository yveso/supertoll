import tests.helpers as helpers


def post(client, payload):
    return helpers.post_json(client, "/auth/register", payload)


def test_all_is_good(client):
    response, data = post(
        client,
        {
            "username": "Test",
            "email": "test@test.org",
            "password": "password123",
        },
    )

    helpers.assert_json_response(response, 201)
    helpers.assert_data(data, "success", "Successfully registered")
    assert data["auth_token"]


def test_username_already_exists(client):
    helpers.add_user(
        username="Test", email="doesnt@matter.com", password="123"
    )
    response, data = post(
        client,
        {
            "username": "Test",
            "email": "test@test.org",
            "password": "password123",
        },
    )

    assert response.status_code == 400
    helpers.assert_data(data, "fail", "User already exists")


def test_email_already_exists(client):
    helpers.add_user(
        username="Who ever", email="already@exists.com", password="123"
    )
    response, data = post(
        client,
        {
            "username": "Test",
            "email": "already@exists.com",
            "password": "password123",
        },
    )

    assert response.status_code == 400
    helpers.assert_data(data, "fail", "User already exists")


def test_empty_payload(client):
    response, data = post(client, {})

    assert response.status_code == 400
    helpers.assert_data(data, "fail", "Invalid payload")


def test_no_username_in_payload(client):
    response, data = post(
        client, {"email": "already@exists.com", "password": "password123"}
    )

    assert response.status_code == 400
    helpers.assert_data(data, "fail", "Invalid payload")


def test_no_email_in_payload(client):
    response, data = post(
        client, {"username": "Test", "password": "password123"}
    )

    assert response.status_code == 400
    helpers.assert_data(data, "fail", "Invalid payload")


def test_no_password_in_payload(client):
    response, data = post(
        client, {"username": "Test", "email": "already@exists.com"}
    )

    assert response.status_code == 400
    helpers.assert_data(data, "fail", "Invalid payload")
