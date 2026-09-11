from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.crm_lead import parse_crm_lead_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.crm_lead import CrmLead
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "pipeline", "opportunity")


def test_migration_235_creates_crm_lead_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/235_crm_lead.py").read_text(encoding="utf-8")
    assert 'revision: str = "235_crm_lead"' in source
    assert 'down_revision: str | None = "234_intervention_outcome"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "crm_lead_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency", "pipeline"):
        assert banned not in source


def test_importlinter_lists_crm_lead_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.crm_leads" in forbidden
    assert "app.models.crm_lead" in forbidden


def test_generated_api_types_include_crm_lead() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "CrmLeadResponse" in source
    assert "CrmLeadCreate" in source


def test_fga_source_declares_crm_lead_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_crm_leads: member" in source


def test_authorization_model_grants_crm_leads_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_crm_leads"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitLeadAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryLeadDesk:
    def __init__(self, session: object) -> None:
        self.leads: list[CrmLead] = []

    async def list_leads(self) -> list[CrmLead]:
        return list(self.leads)

    async def persist_crm_lead(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        lead_code: object,
        stage_kind: object,
        source_ref: object,
    ) -> CrmLead:
        code, kind, origin = parse_crm_lead_row(lead_code, stage_kind, source_ref)
        row = CrmLead(
            id=uuid4(),
            organization_id=organization_id,
            lead_code=code,
            stage_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.leads.append(row)
        return row


@pytest.fixture
def lead_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryLeadDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr("app.api.crm_leads.CrmLeadService", lambda _s: desk)
    set_authz_checker(PermitLeadAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "lead_code": "lead_acme_01",
        "stage_kind": "new",
        "source_ref": "fixture://crm-lead/a",
    }
    body.update(extra)
    return body


def test_post_crm_lead_persists(lead_http: object) -> None:
    client, desk = lead_http
    response = client.post(
        "/api/v1/crm-leads",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["stage_kind"] == "new"
    assert len(desk.leads) == 1


def test_post_crm_lead_rejects_amount_pipeline(lead_http: object) -> None:
    client, _desk = lead_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/crm-leads",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_crm_lead_rejects_bad_kind(lead_http: object) -> None:
    client, _desk = lead_http
    response = client.post(
        "/api/v1/crm-leads",
        headers=bearer_auth_headers(),
        json=_payload(stage_kind="cold_send"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_crm_lead_rejects_foreign_source_ref(lead_http: object) -> None:
    client, _desk = lead_http
    response = client.post(
        "/api/v1/crm-leads",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_crm_leads_lists_rows(lead_http: object) -> None:
    client, desk = lead_http
    client.post(
        "/api/v1/crm-leads",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/crm-leads",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.leads) == 1
