from datetime import date
from decimal import Decimal
from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.version_window import VersionWindow
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]


def test_migration_355_creates_version_window_view() -> None:
    source = (_ROOT / "backend/alembic/versions/355_version_window.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "355_version_window"' in source
    assert 'down_revision: str | None = "354_version_score"' in source
    assert "CREATE VIEW version_window" in source
    assert "security_invoker" in source
    assert "created_on" in source
    assert "avg(i.mae)" in source
    assert "prediction_ledger" not in source
    for banned in ("float(", "httpx", "brier", "champion"):
        assert banned not in source.lower()


def test_service_does_not_compute_or_import_ledgers() -> None:
    source = (
        _ROOT / "backend/app/services/version_windows/version_window_service.py"
    ).read_text(encoding="utf-8")
    assert "float" not in source
    assert "prediction_ledgers" not in source
    assert "version_scores" not in source
    assert "interval_scores" not in source
    assert "persist" not in source
    assert "add(" not in source


def test_importlinter_lists_version_window_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.version_windows" in forbidden
    assert "app.models.version_window" in forbidden


def test_api_types_include_version_window() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "VersionWindowResponse" in source
    assert "VersionWindowCreate" not in source


def test_fga_source_declares_version_window_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_version_windows: member" in source


def test_fga_model_grants_version_window_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_version_windows"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitVersionWindowAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryVersionWindowDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[VersionWindow] = []

    async def list_rows(self) -> list[VersionWindow]:
        return list(self.rows)


@pytest.fixture
def version_window_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryVersionWindowDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.version_windows.VersionWindowService",
        lambda _s: desk,
    )
    set_authz_checker(PermitVersionWindowAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_get_lists_daily_averages(version_window_http: object) -> None:
    client, desk = version_window_http
    desk.rows.append(
        VersionWindow(
            organization_id=uuid4(),
            model_version="hist_eta",
            created_on=date(2026, 9, 13),
            pair_count=2,
            avg_mae=Decimal("1.0000"),
            avg_crps=Decimal("1.2500"),
        )
    )
    response = client.get(
        "/api/v1/version-windows",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    body = response.json()
    assert body[0]["model_version"] == "hist_eta"
    assert body[0]["created_on"] == "2026-09-13"
    assert body[0]["pair_count"] == 2
    assert body[0]["avg_mae"] == "1.0000"
    assert body[0]["avg_crps"] == "1.2500"


def test_post_is_rejected(version_window_http: object) -> None:
    client, _desk = version_window_http
    response = client.post(
        "/api/v1/version-windows",
        headers=bearer_auth_headers(),
        json={"avg_crps": "0.1", "drift": True},
    )
    assert response.status_code == 405
