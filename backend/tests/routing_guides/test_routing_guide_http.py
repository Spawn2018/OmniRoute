from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.routing_guide import parse_routing_guide_row
from app.main import app
from app.models.routing_guide import RoutingGuide
from tests.http_auth import bearer_auth_headers

_FORBIDDEN = ("shipment_id", "blocks_dispatch", "amount", "currency", "buy_amount")


class PermitRoutingGuideAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryRoutingGuideDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.guides: list[RoutingGuide] = []

    async def list_guides(self) -> list[RoutingGuide]:
        return list(self.guides)

    async def persist_routing_guide(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        guide_code: object,
        lane_label: object,
        mode_label: object,
        source_ref: object,
    ) -> RoutingGuide:
        code, lane, mode, origin = parse_routing_guide_row(
            guide_code, lane_label, mode_label, source_ref
        )
        row = RoutingGuide(
            id=uuid4(),
            organization_id=organization_id,
            guide_code=code,
            lane_label=lane,
            mode_label=mode,
            source_ref=origin,
            created_by=user_id,
        )
        self.guides.append(row)
        return row


@pytest.fixture
def routing_guide_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryRoutingGuideDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr("app.api.routing_guides.RoutingGuideService", lambda _s: desk)
    set_authz_checker(PermitRoutingGuideAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "guide_code": "guide_pl_de",
        "lane_label": "Gdańsk–Hamburg",
        "mode_label": "road",
        "source_ref": "fixture://routing-guide/pl-1",
    }
    body.update(extra)
    return body


def test_http_lists_and_creates_routing_guide(routing_guide_http: object) -> None:
    client, _desk = routing_guide_http
    created = client.post(
        "/api/v1/routing-guides",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert created.status_code == 201
    assert created.json()["guide_code"] == "guide_pl_de"
    listed = client.get("/api/v1/routing-guides", headers=bearer_auth_headers())
    assert listed.status_code == 200
    assert len(listed.json()) == 1


def test_http_rejects_bad_guide_code(routing_guide_http: object) -> None:
    client, _desk = routing_guide_http
    response = client.post(
        "/api/v1/routing-guides",
        headers=bearer_auth_headers(),
        json=_payload(guide_code="X"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


@pytest.mark.parametrize("field", _FORBIDDEN)
def test_http_forbids_shipment_and_money_fields(
    routing_guide_http: object, field: str
) -> None:
    client, _desk = routing_guide_http
    body = _payload()
    body[field] = "x"
    response = client.post(
        "/api/v1/routing-guides",
        headers=bearer_auth_headers(),
        json=body,
    )
    assert response.status_code == 422
