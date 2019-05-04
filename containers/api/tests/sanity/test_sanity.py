import json


def test_get_status_code(client):
    resp = client.get("/sanity/")
    assert resp.status_code == 200


def test_get_data(client):
    resp = client.get("/sanity/")
    from_json = json.loads(resp.data)
    assert "message" in from_json
    assert from_json["message"] == "Relax"
