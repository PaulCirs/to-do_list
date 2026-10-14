import os

# Les tests utilisent leur propre base, jetable, avant d'importer l'appli.
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


def test_health():
    with TestClient(app) as client:
        assert client.get("/health").json() == {"status": "ok"}


def test_todo_lifecycle():
    with TestClient(app) as client:
        # Créer
        created = client.post("/api/todos", json={"title": "Apprendre Docker"})
        assert created.status_code == 201
        todo_id = created.json()["id"]

        # Lister
        titles = [t["title"] for t in client.get("/api/todos").json()]
        assert "Apprendre Docker" in titles

        # Cocher
        updated = client.patch(f"/api/todos/{todo_id}", json={"done": True})
        assert updated.json()["done"] is True

        # Supprimer
        assert client.delete(f"/api/todos/{todo_id}").status_code == 204
        assert client.delete(f"/api/todos/{todo_id}").status_code == 404


def test_empty_title_is_rejected():
    with TestClient(app) as client:
        assert client.post("/api/todos", json={"title": ""}).status_code == 422
