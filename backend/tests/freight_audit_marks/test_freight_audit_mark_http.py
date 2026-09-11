from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.freight_audit_mark import parse_freight_audit_mark_row
from app.main import app
from app.models.freight_audit_mark import FreightAuditMark
from tests.http_auth import bearer_auth_headers

_FORBIDDEN = ("amount", "margin", "buy_amount", "shipment_id")


class PermitFreightAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryFreightDesk:
    def __init__(self, session: object) -> None:
        self.marks: list[FreightAuditMark] = []

    async def list_marks(self) -> list[FreightAuditMark]:
        return list(self.marks)

    async def persist_freight_audit_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        audit_kind: object,
        source_ref: object,
    ) -> FreightAuditMark:
        code, kind, origin = parse_freight_audit_mark_row(
            mark_code, audit_kind, source_ref
        )
        row = FreightAuditMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            audit_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.marks.append(row)
        return row


@pytest.fixture
def freight_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryFreightDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.freight_audit_marks.FreightAuditMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitFreightAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "audit_inv_01",
        "audit_kind": "expected_vs_invoice",
        "source_ref": "fixture://freight-audit-mark/pl-1",
    }
    body.update(extra)
    return body


def test_http_lists_and_creates_freight_audit_mark(freight_http: object) -> None:
    client, _desk = freight_http
    created = client.post(
        "/api/v1/freight-audit-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert created.status_code == 201
    listed = client.get(
        "/api/v1/freight-audit-marks",
        headers=bearer_auth_headers(),
    )
    assert listed.status_code == 200
    assert len(listed.json()) == 1


@pytest.mark.parametrize("field", _FORBIDDEN)
def test_http_forbids_money_fields(freight_http: object, field: str) -> None:
    client, _desk = freight_http
    body = _payload()
    body[field] = "x"
    response = client.post(
        "/api/v1/freight-audit-marks",
        headers=bearer_auth_headers(),
        json=body,
    )
    assert response.status_code == 422
