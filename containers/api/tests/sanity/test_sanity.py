import json


def test_sanity_status_code(app):
    client = app.test_client()

    resp = client.get("/sanity/")
    assert resp.status_code == 200


def test_sanity_data(app):
    client = app.test_client()

    resp = client.get("/sanity/")
    from_json = json.loads(resp.data)
    assert "message" in from_json
    assert from_json["message"] == "Relax"
