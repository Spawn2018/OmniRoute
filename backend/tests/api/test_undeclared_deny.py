from fastapi.testclient import TestClient

from app.main import app


def test_docs_playground_is_off() -> None:
    client = TestClient(app)
    assert client.get("/docs").status_code == 404
    assert client.get("/redoc").status_code == 404
    assert client.get("/openapi.json").status_code == 404


def test_health_stays_public() -> None:
    response = TestClient(app).get("/health")
    assert response.status_code == 200


def test_undeclared_api_v1_path_is_denied() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/this-route-is-not-declared")
    assert response.status_code == 403
    assert response.json()["detail"] == "Brak deklaracji uprawnień"


def test_undeclared_api_v1_post_is_denied() -> None:
    response = TestClient(app).post("/api/v1/also-not-declared")
    assert response.status_code == 403
