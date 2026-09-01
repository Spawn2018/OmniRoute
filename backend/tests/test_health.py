from uuid import UUID

from fastapi.testclient import TestClient
from pytest import MonkeyPatch
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import probe_database
from app.main import app


def test_health_returns_ok() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    UUID(response.headers["X-Request-ID"])


def test_health_echoes_valid_request_id() -> None:
    request_id = "550e8400-e29b-41d4-a716-446655440000"
    response = TestClient(app).get("/health", headers={"X-Request-ID": request_id})
    assert response.headers["X-Request-ID"] == request_id


def test_health_replaces_invalid_request_id() -> None:
    response = TestClient(app).get("/health", headers={"X-Request-ID": "not-a-uuid"})
    generated = response.headers["X-Request-ID"]
    UUID(generated)
    assert generated != "not-a-uuid"


def test_ready_ok_when_database_probes(monkeypatch: MonkeyPatch) -> None:
    async def ok() -> bool:
        return True

    monkeypatch.setattr("app.main.probe_database", ok)
    response = TestClient(app).get("/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    UUID(response.headers["X-Request-ID"])


async def test_probe_database_true_on_select(monkeypatch: MonkeyPatch) -> None:
    class _Conn:
        async def execute(self, _stmt: object) -> object:
            return object()

    class _Up:
        async def __aenter__(self) -> _Conn:
            return _Conn()

        async def __aexit__(self, *_args: object) -> bool:
            return False

    class _Engine:
        def connect(self) -> _Up:
            return _Up()

    monkeypatch.setattr("app.core.database.engine", _Engine())
    assert await probe_database() is True


async def test_probe_database_false_on_sql_error(monkeypatch: MonkeyPatch) -> None:
    class _Down:
        async def __aenter__(self) -> None:
            raise SQLAlchemyError("down")

        async def __aexit__(self, *_args: object) -> bool:
            return False

    class _Engine:
        def connect(self) -> _Down:
            return _Down()

    monkeypatch.setattr("app.core.database.engine", _Engine())
    assert await probe_database() is False


def test_ready_unavailable_when_database_down(monkeypatch: MonkeyPatch) -> None:
    async def down() -> bool:
        return False

    monkeypatch.setattr("app.main.probe_database", down)
    response = TestClient(app).get("/ready")
    assert response.status_code == 503
    assert response.json() == {"status": "not_ready"}
