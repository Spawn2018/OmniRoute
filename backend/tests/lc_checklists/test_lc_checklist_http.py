from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.lc_checklist import parse_lc_checklist_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.lc_checklist import LcChecklist
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "due", "presentation_due")


def test_migration_236_creates_lc_checklist_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/236_lc_checklist.py").read_text(encoding="utf-8")
    assert 'revision: str = "236_lc_checklist"' in source
    assert 'down_revision: str | None = "235_crm_lead"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "lc_checklist_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency", "pipeline"):
        assert banned not in source


def test_importlinter_lists_lc_checklist_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.lc_checklists" in forbidden
    assert "app.models.lc_checklist" in forbidden


def test_generated_api_types_include_lc_checklist() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "LcChecklistResponse" in source
    assert "LcChecklistCreate" in source


def test_fga_source_declares_lc_checklist_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_lc_checklists: member" in source


def test_authorization_model_grants_lc_checklists_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_lc_checklists"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitLcAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryLcDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[LcChecklist] = []

    async def list_checklists(self) -> list[LcChecklist]:
        return list(self.rows)

    async def persist_lc_checklist(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        checklist_code: object,
        status_kind: object,
        source_ref: object,
    ) -> LcChecklist:
        code, kind, origin = parse_lc_checklist_row(
            checklist_code,
            status_kind,
            source_ref,
        )
        row = LcChecklist(
            id=uuid4(),
            organization_id=organization_id,
            checklist_code=code,
            status_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def lc_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryLcDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr("app.api.lc_checklists.LcChecklistService", lambda _s: desk)
    set_authz_checker(PermitLcAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "checklist_code": "lc_acme_01",
        "status_kind": "open",
        "source_ref": "fixture://lc-checklist/a",
    }
    body.update(extra)
    return body


def test_post_lc_checklist_persists(lc_http: object) -> None:
    client, desk = lc_http
    response = client.post(
        "/api/v1/lc-checklists",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["status_kind"] == "open"
    assert len(desk.rows) == 1


def test_post_lc_checklist_rejects_amount_due(lc_http: object) -> None:
    client, _desk = lc_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/lc-checklists",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_lc_checklist_rejects_bad_kind(lc_http: object) -> None:
    client, _desk = lc_http
    response = client.post(
        "/api/v1/lc-checklists",
        headers=bearer_auth_headers(),
        json=_payload(status_kind="bank_live"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_lc_checklist_rejects_foreign_source_ref(lc_http: object) -> None:
    client, _desk = lc_http
    response = client.post(
        "/api/v1/lc-checklists",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lc_checklists_lists_rows(lc_http: object) -> None:
    client, desk = lc_http
    client.post(
        "/api/v1/lc-checklists",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/lc-checklists",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
