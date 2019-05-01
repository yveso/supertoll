import json


def test_users_ping_get(app):
    client = app.test_client()

    resp = client.get("/users/ping")
    from_json = json.loads(resp.data)
    assert resp.status_code == 200
    assert "message" in from_json
    assert from_json["message"] == "hooray"
