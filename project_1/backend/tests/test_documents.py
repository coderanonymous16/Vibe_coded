from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_documents_endpoint_returns_catalog() -> None:
    response = client.get("/api/v1/documents")
    assert response.status_code == 200
    payload = response.json()
    assert "documents" in payload
    assert payload["documents"]


def test_subjects_endpoint_returns_subjects() -> None:
    response = client.get("/api/v1/subjects")
    assert response.status_code == 200
    payload = response.json()
    assert "subjects" in payload
    assert any(subject["name"] == "DBMS" for subject in payload["subjects"])
