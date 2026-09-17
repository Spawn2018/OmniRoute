from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.self_billing_mark import parse_self_billing_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.self_billing_mark import SelfBillingMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "bytes")


def test_migration_428_creates_self_billing_mark_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/428_self_billing_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "428_self_billing_mark"' in source
    assert 'down_revision: str | None = "427_od_product_ticket"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "self_billing_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency", "bytes"):
        assert banned not in source


def test_importlinter_lists_self_billing_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.self_billing_marks" in forbidden
    assert "app.models.self_billing_mark" in forbidden


def test_fga_source_declares_self_billing_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_self_billing_marks: member" in source


def test_authorization_model_grants_self_billing_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_self_billing_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[SelfBillingMark] = []

    async def list_marks(self) -> list[SelfBillingMark]:
        return list(self.rows)

    async def persist_self_billing_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        billing_kind: object,
        source_ref: object,
    ) -> SelfBillingMark:
        code, kind, origin = parse_self_billing_mark_row(
            mark_code,
            billing_kind,
            source_ref,
        )
        row = SelfBillingMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            billing_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def self_billing_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.self_billing_marks.SelfBillingMarkService",
        lambda _session: desk,
    )
    set_authz_checker(PermitAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "self_01",
        "billing_kind": "self",
        "source_ref": "fixture://self-billing-mark/a",
    }
    body.update(extra)
    return body


def test_post_self_billing_mark_persists(self_billing_http: object) -> None:
    client, desk = self_billing_http
    response = client.post(
        "/api/v1/self-billing-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["billing_kind"] == "self"
    assert len(desk.rows) == 1


def test_post_self_billing_mark_rejects_amount_bytes(self_billing_http: object) -> None:
    client, _desk = self_billing_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/self-billing-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_self_billing_mark_rejects_bad_kind(self_billing_http: object) -> None:
    client, _desk = self_billing_http
    response = client.post(
        "/api/v1/self-billing-marks",
        headers=bearer_auth_headers(),
        json=_payload(billing_kind="stripe"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_get_self_billing_marks_lists_rows(self_billing_http: object) -> None:
    client, desk = self_billing_http
    client.post(
        "/api/v1/self-billing-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/self-billing-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
