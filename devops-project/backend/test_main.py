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


def test_delete_task():
    # Créer une tâche puis la supprimer
    create = client.post("/api/tasks", json={"title": "À supprimer"})
    task_id = create.json()["id"]

    response = client.delete(f"/api/tasks/{task_id}")
    assert response.status_code == 204

    # Vérifier qu'elle n'existe plus dans la liste
    tasks = client.get("/api/tasks").json()
    assert all(t["id"] != task_id for t in tasks)


def test_delete_task_not_found():
    response = client.delete("/api/tasks/99999")
    assert response.status_code == 404


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
