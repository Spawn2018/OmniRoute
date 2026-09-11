from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.clause_notice import parse_clause_notice_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.clause_notice import ClauseNotice
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("shipment_id", "amount")


def test_migration_229_creates_clause_notice_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/229_clause_notice.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "229_clause_notice"' in source
    assert 'down_revision: str | None = "228_impact_scenario"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "clause_notice_tenant_isolation" in source


def test_importlinter_lists_clause_notice_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.clause_notices" in forbidden
    assert "app.models.clause_notice" in forbidden


def test_generated_api_types_include_clause_notice() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "ClauseNoticeResponse" in source
    assert "ClauseNoticeCreate" in source


def test_fga_source_declares_clause_notice_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_clause_notices: member" in source


def test_authorization_model_grants_clause_notices_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_clause_notices"]
    assert relation.computed_userset is not None


class PermitClauseAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryClauseDesk:
    def __init__(self, session: object) -> None:
        self.notices: list[ClauseNotice] = []

    async def list_notices(self) -> list[ClauseNotice]:
        return list(self.notices)

    async def persist_clause_notice(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        notice_code: object,
        clause_label: object,
        source_ref: object,
    ) -> ClauseNotice:
        code, label, origin = parse_clause_notice_row(
            notice_code, clause_label, source_ref
        )
        row = ClauseNotice(
            id=uuid4(),
            organization_id=organization_id,
            notice_code=code,
            clause_label=label,
            source_ref=origin,
            created_by=user_id,
        )
        self.notices.append(row)
        return row


@pytest.fixture
def clause_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryClauseDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.clause_notices.ClauseNoticeService",
        lambda _s: desk,
    )
    set_authz_checker(PermitClauseAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "notice_code": "late_delivery_01",
        "clause_label": "late delivery notice",
        "source_ref": "fixture://clause-notice/a",
    }
    body.update(extra)
    return body


def test_post_clause_notice_persists(clause_http: object) -> None:
    client, desk = clause_http
    response = client.post(
        "/api/v1/clause-notices",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["clause_label"] == "late delivery notice"
    assert len(desk.notices) == 1


def test_post_clause_notice_rejects_extra(clause_http: object) -> None:
    client, _desk = clause_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/clause-notices",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_clause_notice_rejects_bad_label(clause_http: object) -> None:
    client, _desk = clause_http
    response = client.post(
        "/api/v1/clause-notices",
        headers=bearer_auth_headers(),
        json=_payload(clause_label=""),
    )
    assert response.status_code == 400
    assert "etykieta" in response.json()["detail"]


def test_post_clause_notice_rejects_foreign_source_ref(clause_http: object) -> None:
    client, _desk = clause_http
    response = client.post(
        "/api/v1/clause-notices",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_clause_notices_lists_rows(clause_http: object) -> None:
    client, desk = clause_http
    client.post(
        "/api/v1/clause-notices",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get("/api/v1/clause-notices", headers=bearer_auth_headers())
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.notices) == 1
