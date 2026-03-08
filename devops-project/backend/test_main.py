from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_tasks():
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_create_task():
    response = client.post("/api/tasks", json={"title": "Nouvelle tâche"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Nouvelle tâche"
    assert data["done"] is False


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
