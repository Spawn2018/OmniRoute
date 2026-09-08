from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.groupage_line import (
    require_cutoff_local,
    require_line_code,
    require_line_source_ref,
    require_line_transit_days,
    require_operating_dows,
)
from app.main import app
from app.models.groupage_line import GroupageLine
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


class _Place:
    def __init__(self, row_id: UUID, kind: str) -> None:
        self.id = row_id
        self.kind = kind


class StubLocationService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.by_id: dict[UUID, _Place] = {}

    async def get_location(self, location_id: UUID) -> _Place:
        found = self.by_id.get(location_id)
        if found is None:
            raise ResourceNotFound("nieznana lokalizacja")
        return found


class StubGroupageLineService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[GroupageLine] = []

    async def list_lines(self) -> list[GroupageLine]:
        return [row for row in self.rows if row.superseded_by is None]

    async def record_line(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        line_code: object,
        origin_location_id: object,
        destination_location_id: object,
        cutoff_local: object,
        transit_days: object,
        operating_dows: object,
        source_ref: object,
    ) -> GroupageLine:
        code = require_line_code(line_code)
        cutoff = require_cutoff_local(cutoff_local)
        days = require_line_transit_days(transit_days)
        dows = require_operating_dows(operating_dows)
        origin_ref = require_line_source_ref(source_ref)
        current = next(
            (row for row in self.rows if row.line_code == code and row.superseded_by is None),
            None,
        )
        if (
            current is not None
            and current.origin_location_id == origin_location_id
            and current.destination_location_id == destination_location_id
            and current.cutoff_local == cutoff
            and current.transit_days == days
            and list(current.operating_dows) == dows
            and current.source_ref == origin_ref
        ):
            return current
        successor = GroupageLine(
            id=uuid4(),
            organization_id=organization_id,
            line_code=code,
            origin_location_id=origin_location_id,
            destination_location_id=destination_location_id,
            cutoff_local=cutoff,
            transit_days=days,
            operating_dows=dows,
            source_ref=origin_ref,
            created_by=user_id,
        )
        if current is not None:
            current.superseded_by = successor.id
        self.rows.append(successor)
        return successor


@pytest.fixture
def line_client(monkeypatch: pytest.MonkeyPatch) -> object:
    places = StubLocationService(object())
    origin = _Place(uuid4(), "postal_zone")
    dest = _Place(uuid4(), "address")
    port = _Place(uuid4(), "unlocode")
    places.by_id = {origin.id: origin, dest.id: dest, port.id: port}
    rows = StubGroupageLineService(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.groupage_lines.LocationService", lambda _s: places)
    monkeypatch.setattr("app.api.groupage_lines.GroupageLineService", lambda _s: rows)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), rows, origin, dest, port
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_list_supersede_and_reject_port(line_client: object) -> None:
    client, _rows, origin, dest, port = line_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    payload = {
        "line_code": "wa_hub",
        "origin_location_id": str(origin.id),
        "destination_location_id": str(dest.id),
        "cutoff_local": "16:00:00",
        "transit_days": 2,
        "operating_dows": [1, 2, 3, 4, 5],
        "source_ref": "tenant:manual",
    }
    first = client.post("/api/v1/groupage-lines", headers=headers, json=payload)
    assert first.status_code == 201
    assert first.json()["organization_id"] == str(org_id)
    assert first.json()["line_code"] == "wa_hub"
    assert "amount" not in first.json()
    second = client.post(
        "/api/v1/groupage-lines",
        headers=headers,
        json={**payload, "transit_days": 3},
    )
    assert second.status_code == 201
    assert second.json()["id"] != first.json()["id"]
    listed = client.get("/api/v1/groupage-lines", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == second.json()["id"]
    zero = client.post(
        "/api/v1/groupage-lines",
        headers=headers,
        json={**payload, "line_code": "other_line", "transit_days": 0},
    )
    assert zero.status_code == 400
    ported = client.post(
        "/api/v1/groupage-lines",
        headers=headers,
        json={**payload, "origin_location_id": str(port.id)},
    )
    assert ported.status_code == 400
    assert "UN/LOCODE" in ported.json()["detail"]
