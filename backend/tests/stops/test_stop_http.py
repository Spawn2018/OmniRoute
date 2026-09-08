from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.stop import (
    require_sequence_no,
    require_stop_kind,
    require_stop_source_ref,
    require_stop_status,
    require_time_zone,
)
from app.main import app
from app.models.location import Location
from app.models.shipment import Shipment
from app.models.stop import Stop
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


class StubShipmentService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: Shipment | None = None

    async def get_shipment(self, shipment_id: UUID) -> Shipment:
        if self.row is None or self.row.id != shipment_id:
            raise ResourceNotFound("nieznane zlecenie")
        return self.row


class StubLocationService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: Location | None = None

    async def get_location(self, location_id: UUID) -> Location:
        if self.row is None or self.row.id != location_id:
            raise ResourceNotFound("nieznana lokalizacja")
        return self.row


class StubStopService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[Stop] = []

    async def list_for_shipment(self, shipment_id: object) -> list[Stop]:
        order_id = shipment_id if type(shipment_id) is UUID else uuid4()
        return [
            row
            for row in self.rows
            if row.shipment_id == order_id and row.superseded_by is None
        ]

    async def record_stop(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: object,
        location_id: object,
        stop_kind: object,
        sequence_no: object,
        time_zone: object,
        status: object,
        source_ref: object,
    ) -> Stop:
        kind = require_stop_kind(stop_kind)
        seq = require_sequence_no(sequence_no)
        zone = require_time_zone(time_zone)
        state = require_stop_status(status)
        origin = require_stop_source_ref(source_ref)
        order_id = shipment_id if type(shipment_id) is UUID else uuid4()
        place_id = location_id if type(location_id) is UUID else uuid4()
        current = next(
            (
                row
                for row in self.rows
                if row.shipment_id == order_id
                and row.sequence_no == seq
                and row.superseded_by is None
            ),
            None,
        )
        if (
            current is not None
            and current.location_id == place_id
            and current.stop_kind == kind
            and current.time_zone == zone
            and current.status == state
            and current.source_ref == origin
        ):
            return current
        successor = Stop(
            id=uuid4(),
            organization_id=organization_id,
            shipment_id=order_id,
            location_id=place_id,
            stop_kind=kind,
            sequence_no=seq,
            time_zone=zone,
            status=state,
            source_ref=origin,
            created_by=user_id,
        )
        if current is not None:
            current.superseded_by = successor.id
        self.rows.append(successor)
        return successor


def _shipment() -> Shipment:
    return Shipment(
        id=uuid4(),
        organization_id=uuid4(),
        quotation_id=uuid4(),
        party_id=uuid4(),
        source_ref="fixture://shipment/1",
        status="draft",
    )


def _place() -> Location:
    return Location(
        id=uuid4(),
        organization_id=uuid4(),
        kind="postal_zone",
        name="Strefa test",
        code="PL-T",
        source_ref="tenant:manual",
    )


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    ships = StubShipmentService(object())
    places = StubLocationService(object())
    rows = StubStopService(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.stops.ShipmentService", lambda _s: ships)
    monkeypatch.setattr("app.api.stops.LocationService", lambda _s: places)
    monkeypatch.setattr("app.api.stops.StopService", lambda _s: rows)
    ships.row = _shipment()
    places.row = _place()
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), ships, places, rows
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_list_supersede_and_reject_pickup(catalog_client: object) -> None:
    client, ships, places, _rows = catalog_client
    assert ships.row is not None
    assert places.row is not None
    headers = bearer_auth_headers()
    payload = {
        "shipment_id": str(ships.row.id),
        "location_id": str(places.row.id),
        "stop_kind": "loading",
        "sequence_no": 1,
        "time_zone": "Europe/Warsaw",
        "status": "pending",
        "source_ref": "tenant:manual",
    }
    first = client.post("/api/v1/stops", headers=headers, json=payload)
    assert first.status_code == 201
    assert "amount" not in first.json()
    second = client.post(
        "/api/v1/stops",
        headers=headers,
        json={**payload, "status": "completed"},
    )
    assert second.status_code == 201
    assert second.json()["id"] != first.json()["id"]
    listed = client.get(
        "/api/v1/stops",
        headers=headers,
        params={"shipment_id": str(ships.row.id)},
    )
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == second.json()["id"]
    pickup = client.post("/api/v1/stops", headers=headers, json={**payload, "stop_kind": "pickup"})
    assert pickup.status_code == 400
    queued = client.post("/api/v1/stops", headers=headers, json={**payload, "status": "queued"})
    assert queued.status_code == 400
