from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.allocation_key import parse_allocation_key_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.allocation_key import AllocationKey
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "margin", "score")


def test_migration_406_creates_allocation_key_and_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/406_allocation_key.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "406_allocation_key"' in source
    assert 'down_revision: str | None = "405_extraction_prompt_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "allocation_key_tenant_isolation" in source
    for banned in ("float(", "httpx", "crps", "mae"):
        assert banned not in source.lower()
    assert "IN (" not in source
    assert "charge" not in source


def test_importlinter_lists_allocation_key_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.allocation_keys" in forbidden
    assert "app.models.allocation_key" in forbidden


def test_api_types_include_allocation_key() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "AllocationKeyResponse" in source
    assert "AllocationKeyCreate" in source


def test_fga_source_declares_allocation_key_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_allocation_keys: member" in source


def test_fga_model_grants_allocation_key_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_allocation_keys"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitAllocationKeyAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryAllocationKeyDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[AllocationKey] = []

    async def list_rows(self) -> list[AllocationKey]:
        return list(self.rows)

    async def persist_key(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        key_code: object,
        source_ref: object,
    ) -> AllocationKey:
        draft = parse_allocation_key_row(key_code, source_ref)
        row = AllocationKey(
            id=uuid4(),
            organization_id=organization_id,
            key_code=draft.key_code,
            source_ref=draft.source_ref,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def allocation_key_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryAllocationKeyDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr("app.api.allocation_keys.AllocationKeyService", lambda _s: desk)
    set_authz_checker(PermitAllocationKeyAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "key_code": "lane_direct",
        "source_ref": "fixture://allocation-key/a",
    }
    body.update(extra)
    return body


def test_post_persists_open_key(allocation_key_http: object) -> None:
    client, desk = allocation_key_http
    response = client.post(
        "/api/v1/allocation-keys",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["key_code"] == "lane_direct"
    assert response.headers.get("X-Omni-Catalog") == "allocation-key"
    assert len(desk.rows) == 1


def test_post_rejects_amount_margin_score(allocation_key_http: object) -> None:
    client, _desk = allocation_key_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/allocation-keys",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_bad_code(allocation_key_http: object) -> None:
    client, _desk = allocation_key_http
    response = client.post(
        "/api/v1/allocation-keys",
        headers=bearer_auth_headers(),
        json=_payload(key_code="1x"),
    )
    assert response.status_code == 400
    assert "kod" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(allocation_key_http: object) -> None:
    client, _desk = allocation_key_http
    response = client.post(
        "/api/v1/allocation-keys",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(allocation_key_http: object) -> None:
    client, desk = allocation_key_http
    client.post("/api/v1/allocation-keys", headers=bearer_auth_headers(), json=_payload())
    response = client.get("/api/v1/allocation-keys", headers=bearer_auth_headers())
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
