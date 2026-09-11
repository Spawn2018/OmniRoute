from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.routing_guide_match import parse_routing_guide_match_row
from app.main import app
from app.models.routing_guide_match import RoutingGuideMatch
from tests.http_auth import bearer_auth_headers

_FORBIDDEN = ("amount", "margin", "shipment_id")


class PermitMatchAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryMatchDesk:
    def __init__(self, session: object) -> None:
        self.marks: list[RoutingGuideMatch] = []

    async def list_marks(self) -> list[RoutingGuideMatch]:
        return list(self.marks)

    async def persist_routing_guide_match(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        match_kind: object,
        source_ref: object,
    ) -> RoutingGuideMatch:
        code, kind, origin = parse_routing_guide_match_row(
            mark_code, match_kind, source_ref
        )
        row = RoutingGuideMatch(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            match_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.marks.append(row)
        return row


@pytest.fixture
def match_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryMatchDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.routing_guide_matches.RoutingGuideMatchService",
        lambda _s: desk,
    )
    set_authz_checker(PermitMatchAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "match_lane_01",
        "match_kind": "lane_label",
        "source_ref": "fixture://routing-guide-match/pl-1",
    }
    body.update(extra)
    return body


def test_http_lists_and_creates_match(match_http: object) -> None:
    client, _desk = match_http
    created = client.post(
        "/api/v1/routing-guide-matches",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert created.status_code == 201
    listed = client.get(
        "/api/v1/routing-guide-matches",
        headers=bearer_auth_headers(),
    )
    assert listed.status_code == 200
    assert len(listed.json()) == 1


@pytest.mark.parametrize("field", _FORBIDDEN)
def test_http_forbids_money_fields(match_http: object, field: str) -> None:
    client, _desk = match_http
    body = _payload()
    body[field] = "x"
    response = client.post(
        "/api/v1/routing-guide-matches",
        headers=bearer_auth_headers(),
        json=body,
    )
    assert response.status_code == 422
