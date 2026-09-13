from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.twin_kind import parse_twin_kind_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.twin_kind import TwinKind
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "margin", "score")


def test_migration_347_creates_twin_kind_and_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/347_twin_kind.py").read_text(encoding="utf-8")
    assert 'revision: str = "347_twin_kind"' in source
    assert 'down_revision: str | None = "346_suggestion_kind"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "twin_kind_tenant_isolation" in source
    for banned in ("float(", "httpx", "crps", "mae"):
        assert banned not in source.lower()
    assert "IN (" not in source
    assert "twin_mark" not in source


def test_importlinter_lists_twin_kind_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.twin_kinds" in forbidden
    assert "app.models.twin_kind" in forbidden


def test_api_types_include_twin_kind() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "TwinKindResponse" in source
    assert "TwinKindCreate" in source


def test_fga_source_declares_twin_kind_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_twin_kinds: member" in source


def test_fga_model_grants_twin_kind_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_twin_kinds"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitTwinKindAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryTwinKindDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[TwinKind] = []

    async def list_rows(self) -> list[TwinKind]:
        return list(self.rows)

    async def persist_kind(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        kind_code: object,
        source_ref: object,
    ) -> TwinKind:
        draft = parse_twin_kind_row(kind_code, source_ref)
        row = TwinKind(
            id=uuid4(),
            organization_id=organization_id,
            kind_code=draft.kind_code,
            source_ref=draft.source_ref,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def twin_kind_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryTwinKindDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr("app.api.twin_kinds.TwinKindService", lambda _s: desk)
    set_authz_checker(PermitTwinKindAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "kind_code": "tender",
        "source_ref": "fixture://twin-kind/a",
    }
    body.update(extra)
    return body


def test_post_persists_open_kind(twin_kind_http: object) -> None:
    client, desk = twin_kind_http
    response = client.post(
        "/api/v1/twin-kinds",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["kind_code"] == "tender"
    assert response.headers.get("X-Omni-Catalog") == "twin-kind"
    assert len(desk.rows) == 1


def test_post_rejects_amount_margin_score(twin_kind_http: object) -> None:
    client, _desk = twin_kind_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/twin-kinds",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_bad_code(twin_kind_http: object) -> None:
    client, _desk = twin_kind_http
    response = client.post(
        "/api/v1/twin-kinds",
        headers=bearer_auth_headers(),
        json=_payload(kind_code="1x"),
    )
    assert response.status_code == 400
    assert "kod" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(twin_kind_http: object) -> None:
    client, _desk = twin_kind_http
    response = client.post(
        "/api/v1/twin-kinds",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(twin_kind_http: object) -> None:
    client, desk = twin_kind_http
    client.post("/api/v1/twin-kinds", headers=bearer_auth_headers(), json=_payload())
    response = client.get("/api/v1/twin-kinds", headers=bearer_auth_headers())
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
