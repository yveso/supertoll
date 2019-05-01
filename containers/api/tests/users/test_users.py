import json


def test_users_post(app):
    client = app.test_client()

    response = client.post(
        "/users",
        data=json.dumps({"username": "John Doe", "email": "john@doe.org"}),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())

    assert response.status_code == 201
    assert "john@doe.org was added!" in data["message"]
    assert "success" in data["status"]
