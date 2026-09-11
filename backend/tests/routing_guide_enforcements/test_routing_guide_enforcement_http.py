from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.routing_guide_enforcement import parse_routing_guide_enforcement_row
from app.main import app
from app.models.routing_guide_enforcement import RoutingGuideEnforcement
from tests.http_auth import bearer_auth_headers

_FORBIDDEN = ("amount", "margin", "shipment_id", "asn_id")


class PermitEnforcementAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryEnforcementDesk:
    def __init__(self, session: object) -> None:
        self.marks: list[RoutingGuideEnforcement] = []

    async def list_marks(self) -> list[RoutingGuideEnforcement]:
        return list(self.marks)

    async def persist_routing_guide_enforcement(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        enforcement_kind: object,
        source_ref: object,
    ) -> RoutingGuideEnforcement:
        code, kind, origin = parse_routing_guide_enforcement_row(
            mark_code, enforcement_kind, source_ref
        )
        row = RoutingGuideEnforcement(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            enforcement_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.marks.append(row)
        return row


@pytest.fixture
def enforcement_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryEnforcementDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.routing_guide_enforcements.RoutingGuideEnforcementService",
        lambda _s: desk,
    )
    set_authz_checker(PermitEnforcementAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "mode_block_01",
        "enforcement_kind": "block_409",
        "source_ref": "fixture://routing-guide-enforcement/pl-1",
    }
    body.update(extra)
    return body


def test_http_lists_and_creates_routing_guide_enforcement(
    enforcement_http: object,
) -> None:
    client, _desk = enforcement_http
    created = client.post(
        "/api/v1/routing-guide-enforcements",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert created.status_code == 201
    listed = client.get(
        "/api/v1/routing-guide-enforcements",
        headers=bearer_auth_headers(),
    )
    assert listed.status_code == 200
    assert len(listed.json()) == 1
    assert listed.json()[0]["enforcement_kind"] == "block_409"


@pytest.mark.parametrize("field", _FORBIDDEN)
def test_http_forbids_money_and_shipment_fields(
    enforcement_http: object, field: str
) -> None:
    client, _desk = enforcement_http
    body = _payload()
    body[field] = "x"
    response = client.post(
        "/api/v1/routing-guide-enforcements",
        headers=bearer_auth_headers(),
        json=body,
    )
    assert response.status_code == 422
