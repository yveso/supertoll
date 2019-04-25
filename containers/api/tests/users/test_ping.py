import json


def test_users_status_code(app):
    client = app.test_client()

    resp = client.get("/users/ping")
    assert resp.status_code == 200


def test_users_data(app):
    client = app.test_client()

    resp = client.get("/users/ping")
    from_json = json.loads(resp.data)
    assert "message" in from_json
    assert from_json["message"] == "hooray"
