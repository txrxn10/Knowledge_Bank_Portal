def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Knowledge Bank API" in response.json()["name"]


def test_health_check(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
