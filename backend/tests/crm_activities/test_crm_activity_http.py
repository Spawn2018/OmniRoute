from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.crm_activity import parse_crm_activity_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.crm_activity import CrmActivity
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "pipeline", "margin")


def test_migration_394_creates_crm_activity_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/394_crm_activity.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "394_crm_activity"' in source
    assert 'down_revision: str | None = "393_compliance_program_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "crm_activity_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency", "pipeline"):
        assert banned not in source


def test_importlinter_lists_crm_activity_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.crm_activities" in forbidden
    assert "app.models.crm_activity" in forbidden


def test_fga_source_declares_crm_activity_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_crm_activities: member" in source


def test_authorization_model_grants_crm_activities_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_crm_activities"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitOpportunityAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryOpportunityDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[CrmActivity] = []

    async def list_activities(self) -> list[CrmActivity]:
        return list(self.rows)

    async def persist_crm_activity(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        activity_code: object,
        activity_kind: object,
        source_ref: object,
    ) -> CrmActivity:
        code, kind, origin = parse_crm_activity_row(
            activity_code,
            activity_kind,
            source_ref,
        )
        row = CrmActivity(
            id=uuid4(),
            organization_id=organization_id,
            activity_code=code,
            activity_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def activity_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryOpportunityDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.crm_activities.CrmActivityService",
        lambda _s: desk,
    )
    set_authz_checker(PermitOpportunityAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "activity_code": "act_call_01",
        "activity_kind": "call",
        "source_ref": "fixture://crm-activity/a",
    }
    body.update(extra)
    return body


def test_post_crm_activity_persists(activity_http: object) -> None:
    client, desk = activity_http
    response = client.post(
        "/api/v1/crm-activities",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["activity_kind"] == "call"
    assert len(desk.rows) == 1


def test_post_crm_activity_rejects_amount_pipeline(activity_http: object) -> None:
    client, _desk = activity_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/crm-activities",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_crm_activity_rejects_bad_kind(activity_http: object) -> None:
    client, _desk = activity_http
    response = client.post(
        "/api/v1/crm-activities",
        headers=bearer_auth_headers(),
        json=_payload(activity_kind="pipeline"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_crm_activity_rejects_foreign_source_ref(
    activity_http: object,
) -> None:
    client, _desk = activity_http
    response = client.post(
        "/api/v1/crm-activities",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_crm_activities_lists_rows(activity_http: object) -> None:
    client, desk = activity_http
    client.post(
        "/api/v1/crm-activities",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/crm-activities",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
