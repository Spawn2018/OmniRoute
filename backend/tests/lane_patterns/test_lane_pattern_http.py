from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.lane_pattern import require_pattern_pair, require_pattern_source_ref
from app.main import app
from app.models.lane_pattern import LanePattern
from tests.http_auth import bearer_auth_headers


class AllowAllAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class StubPatternDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[LanePattern] = []

    async def list_patterns(self) -> list[LanePattern]:
        return list(self.rows)

    async def persist_pattern(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        origin_unlocode: object,
        destination_unlocode: object,
        source_ref: object,
    ) -> LanePattern:
        origin, dest = require_pattern_pair(origin_unlocode, destination_unlocode)
        row = LanePattern(
            id=uuid4(),
            organization_id=organization_id,
            origin_unlocode=origin,
            destination_unlocode=dest,
            source_ref=require_pattern_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    patterns = StubPatternDesk(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.lane_patterns.LanePatternService",
        lambda _s: patterns,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), patterns
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "origin_unlocode": "PLGDY",
        "destination_unlocode": "DEHAM",
        "source_ref": "fixture://lane-pattern/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_lane_pattern(catalog_client: object) -> None:
    client, _patterns = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post("/api/v1/lane-patterns", headers=headers, json=_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["origin_unlocode"] == "PLGDY"
    assert body["destination_unlocode"] == "DEHAM"
    assert "buy_amount" not in body
    listed = client.get("/api/v1/lane-patterns", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_same_ends_is_400(catalog_client: object) -> None:
    client, _patterns = catalog_client
    response = client.post(
        "/api/v1/lane-patterns",
        headers=bearer_auth_headers(),
        json=_payload(destination_unlocode="PLGDY"),
    )
    assert response.status_code == 400
    assert "wzorzec" in response.json()["detail"]


def test_http_create_pattern_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _patterns = catalog_client
    response = client.post(
        "/api/v1/lane-patterns",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://hold.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
