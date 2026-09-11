from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.ncts_draft import parse_ncts_draft_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.ncts_draft import NctsDraft
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "xml")


def test_migration_237_creates_ncts_draft_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/237_ncts_draft.py").read_text(encoding="utf-8")
    assert 'revision: str = "237_ncts_draft"' in source
    assert 'down_revision: str | None = "236_lc_checklist"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "ncts_draft_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency", "puesc"):
        assert banned not in source


def test_importlinter_lists_ncts_draft_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.ncts_drafts" in forbidden
    assert "app.models.ncts_draft" in forbidden


def test_generated_api_types_include_ncts_draft() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "NctsDraftResponse" in source
    assert "NctsDraftCreate" in source


def test_fga_source_declares_ncts_draft_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_ncts_drafts: member" in source


def test_authorization_model_grants_ncts_drafts_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_ncts_drafts"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitNctsAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryNctsDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[NctsDraft] = []

    async def list_drafts(self) -> list[NctsDraft]:
        return list(self.rows)

    async def persist_ncts_draft(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        draft_code: object,
        transit_kind: object,
        source_ref: object,
    ) -> NctsDraft:
        code, kind, origin = parse_ncts_draft_row(
            draft_code,
            transit_kind,
            source_ref,
        )
        row = NctsDraft(
            id=uuid4(),
            organization_id=organization_id,
            draft_code=code,
            transit_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def ncts_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryNctsDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr("app.api.ncts_drafts.NctsDraftService", lambda _s: desk)
    set_authz_checker(PermitNctsAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "draft_code": "ncts_t1_01",
        "transit_kind": "t1",
        "source_ref": "fixture://ncts-draft/a",
    }
    body.update(extra)
    return body


def test_post_ncts_draft_persists(ncts_http: object) -> None:
    client, desk = ncts_http
    response = client.post(
        "/api/v1/ncts-drafts",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["transit_kind"] == "t1"
    assert len(desk.rows) == 1


def test_post_ncts_draft_rejects_amount_xml(ncts_http: object) -> None:
    client, _desk = ncts_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/ncts-drafts",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_ncts_draft_rejects_bad_kind(ncts_http: object) -> None:
    client, _desk = ncts_http
    response = client.post(
        "/api/v1/ncts-drafts",
        headers=bearer_auth_headers(),
        json=_payload(transit_kind="puesc_live"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_ncts_draft_rejects_foreign_source_ref(ncts_http: object) -> None:
    client, _desk = ncts_http
    response = client.post(
        "/api/v1/ncts-drafts",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_ncts_drafts_lists_rows(ncts_http: object) -> None:
    client, desk = ncts_http
    client.post(
        "/api/v1/ncts-drafts",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/ncts-drafts",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
