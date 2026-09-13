from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.autonomy_level import parse_autonomy_level_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.autonomy_level import AutonomyLevel
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "margin", "score")


def test_migration_348_creates_autonomy_level_and_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/348_autonomy_level.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "348_autonomy_level"' in source
    assert 'down_revision: str | None = "347_twin_kind"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "autonomy_level_tenant_isolation" in source
    for banned in ("float(", "httpx", "crps", "mae"):
        assert banned not in source.lower()
    assert "IN (" not in source
    assert "party" not in source


def test_importlinter_lists_autonomy_level_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.autonomy_levels" in forbidden
    assert "app.models.autonomy_level" in forbidden


def test_api_types_include_autonomy_level() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "AutonomyLevelResponse" in source
    assert "AutonomyLevelCreate" in source


def test_fga_source_declares_autonomy_level_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_autonomy_levels: member" in source


def test_fga_model_grants_autonomy_level_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_autonomy_levels"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitAutonomyLevelAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryAutonomyLevelDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[AutonomyLevel] = []

    async def list_rows(self) -> list[AutonomyLevel]:
        return list(self.rows)

    async def persist_level(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        level_code: object,
        source_ref: object,
    ) -> AutonomyLevel:
        draft = parse_autonomy_level_row(level_code, source_ref)
        row = AutonomyLevel(
            id=uuid4(),
            organization_id=organization_id,
            level_code=draft.level_code,
            source_ref=draft.source_ref,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def autonomy_level_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryAutonomyLevelDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr("app.api.autonomy_levels.AutonomyLevelService", lambda _s: desk)
    set_authz_checker(PermitAutonomyLevelAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "level_code": "observer",
        "source_ref": "fixture://autonomy-level/a",
    }
    body.update(extra)
    return body


def test_post_persists_open_level(autonomy_level_http: object) -> None:
    client, desk = autonomy_level_http
    response = client.post(
        "/api/v1/autonomy-levels",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["level_code"] == "observer"
    assert response.headers.get("X-Omni-Catalog") == "autonomy-level"
    assert len(desk.rows) == 1


def test_post_rejects_amount_margin_score(autonomy_level_http: object) -> None:
    client, _desk = autonomy_level_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/autonomy-levels",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_bad_code(autonomy_level_http: object) -> None:
    client, _desk = autonomy_level_http
    response = client.post(
        "/api/v1/autonomy-levels",
        headers=bearer_auth_headers(),
        json=_payload(level_code="1x"),
    )
    assert response.status_code == 400
    assert "kod" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(autonomy_level_http: object) -> None:
    client, _desk = autonomy_level_http
    response = client.post(
        "/api/v1/autonomy-levels",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(autonomy_level_http: object) -> None:
    client, desk = autonomy_level_http
    client.post("/api/v1/autonomy-levels", headers=bearer_auth_headers(), json=_payload())
    response = client.get("/api/v1/autonomy-levels", headers=bearer_auth_headers())
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
