import pytest
from main import app
from database import init_db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["DATABASE_URL"] = "sqlite:///:memory:"
    app.config["BASE_URL"] = "http://localhost:8080"
    init_db(app.config["DATABASE_URL"])
    with app.test_client() as client:
        yield client


def test_ping(client):
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "pong"


def test_create_link(client):
    payload = {"original_url": "https://example.com/long-url", "short_name": "exmpl"}
    response = client.post("/api/links", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["id"] == 1
    assert data["original_url"] == "https://example.com/long-url"
    assert data["short_name"] == "exmpl"
    assert data["short_url"] == "http://localhost:8080/r/exmpl"


def test_list_links(client):
    client.post("/api/links", json={"original_url": "https://a.com", "short_name": "a"})
    client.post("/api/links", json={"original_url": "https://b.com", "short_name": "b"})
    response = client.get("/api/links")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]["short_name"] == "a"
    assert data[1]["short_name"] == "b"


def test_get_link(client):
    client.post(
        "/api/links",
        json={"original_url": "https://example.com", "short_name": "ex"},
    )
    response = client.get("/api/links/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["short_name"] == "ex"


def test_get_link_not_found(client):
    response = client.get("/api/links/999")
    assert response.status_code == 404
    assert response.get_json() == {"error": "Not found"}


def test_update_link(client):
    client.post(
        "/api/links",
        json={"original_url": "https://old.com", "short_name": "old"},
    )
    response = client.put(
        "/api/links/1",
        json={"original_url": "https://new.com", "short_name": "new"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["original_url"] == "https://new.com"
    assert data["short_name"] == "new"


def test_update_link_not_found(client):
    response = client.put(
        "/api/links/999",
        json={"original_url": "https://x.com", "short_name": "x"},
    )
    assert response.status_code == 404


def test_delete_link(client):
    client.post(
        "/api/links",
        json={"original_url": "https://example.com", "short_name": "del"},
    )
    response = client.delete("/api/links/1")
    assert response.status_code == 204
    assert response.data == b""
    get_resp = client.get("/api/links/1")
    assert get_resp.status_code == 404


def test_delete_link_not_found(client):
    response = client.delete("/api/links/999")
    assert response.status_code == 404


def test_duplicate_short_name(client):
    client.post(
        "/api/links",
        json={"original_url": "https://a.com", "short_name": "dup"},
    )
    response = client.post(
        "/api/links",
        json={"original_url": "https://b.com", "short_name": "dup"},
    )
    assert response.status_code == 422
    assert response.get_json() == {"error": "short_name must be unique"}


def test_update_duplicate_short_name(client):
    client.post("/api/links", json={"original_url": "https://a.com", "short_name": "a"})
    client.post("/api/links", json={"original_url": "https://b.com", "short_name": "b"})
    response = client.put(
        "/api/links/1",
        json={"short_name": "b"},
    )
    assert response.status_code == 422
    assert response.get_json() == {"error": "short_name must be unique"}
