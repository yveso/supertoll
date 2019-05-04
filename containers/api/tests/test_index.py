from tests.helpers import add_user


def test_get_no_users(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Alle User:" in response.data
    assert b"<p>Keine User</p>" in response.data


def test_get_with_users(client):
    add_user("Max Mustermann", "test@test.org")
    add_user("Foo Bar", "foo@bar.com")

    response = client.get("/")

    assert response.status_code == 200
    assert b"Alle User:" in response.data
    assert b"<li>Max Mustermann</li>" in response.data
    assert b"<li>Foo Bar</li>" in response.data
