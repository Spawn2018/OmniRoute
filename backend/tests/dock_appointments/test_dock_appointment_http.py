from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.dock_appointment import (
    require_appointment_code,
    require_appointment_status,
    require_dock_source_ref,
    require_dock_window,
    require_window_date,
)
from app.domain.errors import ResourceNotFound
from app.main import app
from app.models.dock_appointment import DockAppointment
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


class StubStopService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: Stop | None = None

    async def get_stop(self, stop_id: UUID) -> Stop:
        if self.row is None or self.row.id != stop_id:
            raise ResourceNotFound("nieznany punkt operacyjny")
        return self.row


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


class StubDockAppointmentService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[DockAppointment] = []

    async def list_appointments(self) -> list[DockAppointment]:
        return list(self.rows)

    async def record_appointment(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: object,
        stop_id: object,
        appointment_code: object,
        appointment_status: object,
        window_date: object,
        window_start_local: object,
        window_end_local: object,
        source_ref: object,
    ) -> DockAppointment:
        start, end = require_dock_window(window_start_local, window_end_local)
        row = DockAppointment(
            id=uuid4(),
            organization_id=organization_id,
            shipment_id=shipment_id if type(shipment_id) is UUID else uuid4(),
            stop_id=stop_id if type(stop_id) is UUID else uuid4(),
            appointment_code=require_appointment_code(appointment_code),
            appointment_status=require_appointment_status(appointment_status),
            window_date=require_window_date(window_date),
            window_start_local=start,
            window_end_local=end,
            source_ref=require_dock_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


def _shipment() -> Shipment:
    return Shipment(
        id=uuid4(),
        organization_id=uuid4(),
        quotation_id=uuid4(),
        party_id=uuid4(),
        source_ref="fixture://shipment/1",
        status="draft",
    )


def _halt(shipment_id: UUID, location_id: UUID) -> Stop:
    return Stop(
        id=uuid4(),
        organization_id=uuid4(),
        shipment_id=shipment_id,
        location_id=location_id,
        stop_kind="unloading",
        sequence_no=1,
        time_zone="Europe/Warsaw",
        status="pending",
        source_ref="fixture://stop/dock",
        eta_physical=datetime(2026, 9, 9, 12, 0, tzinfo=UTC),
        eta_legal=datetime(2026, 9, 9, 12, 0, tzinfo=UTC),
    )


@pytest.fixture
def dock_client(monkeypatch: pytest.MonkeyPatch) -> object:
    ships = StubShipmentService(object())
    halts = StubStopService(object())
    places = StubLocationService(object())
    docks = StubDockAppointmentService(object())
    ships.row = _shipment()
    assert ships.row is not None
    place_id = uuid4()
    places.by_id[place_id] = _Place(place_id, "postal_zone")
    halts.row = _halt(ships.row.id, place_id)

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.dock_appointments.ShipmentService", lambda _s: ships)
    monkeypatch.setattr("app.api.dock_appointments.StopService", lambda _s: halts)
    monkeypatch.setattr("app.api.dock_appointments.LocationService", lambda _s: places)
    monkeypatch.setattr("app.api.dock_appointments.DockAppointmentService", lambda _s: docks)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), ships, halts, places
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(ships: StubShipmentService, halts: StubStopService) -> dict[str, object]:
    assert ships.row is not None
    assert halts.row is not None
    return {
        "shipment_id": str(ships.row.id),
        "stop_id": str(halts.row.id),
        "appointment_code": "dock_1",
        "appointment_status": "advised",
        "window_date": "2026-09-09",
        "window_start_local": "08:00:00",
        "window_end_local": "10:00:00",
        "source_ref": "tenant:manual",
    }


def test_http_create_list_and_reject_backwards_window(dock_client: object) -> None:
    client, ships, halts, _places = dock_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/dock-appointments",
        headers=headers,
        json=_payload(ships, halts),
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["appointment_code"] == "dock_1"
    assert "amount" not in body
    listed = client.get("/api/v1/dock-appointments", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]
    backwards = client.post(
        "/api/v1/dock-appointments",
        headers=headers,
        json={
            **_payload(ships, halts),
            "appointment_code": "dock_2",
            "window_start_local": "11:00:00",
            "window_end_local": "10:00:00",
        },
    )
    assert backwards.status_code == 400
    assert "okno" in backwards.json()["detail"]


def test_http_stop_off_route_is_400(dock_client: object) -> None:
    client, ships, halts, _places = dock_client
    assert halts.row is not None
    halts.row.shipment_id = uuid4()
    response = client.post(
        "/api/v1/dock-appointments",
        headers=bearer_auth_headers(),
        json=_payload(ships, halts),
    )
    assert response.status_code == 400
    assert "trasy" in response.json()["detail"]


def test_http_unlocode_stop_is_400(dock_client: object) -> None:
    client, ships, halts, places = dock_client
    assert halts.row is not None
    places.by_id[halts.row.location_id] = _Place(halts.row.location_id, "unlocode")
    response = client.post(
        "/api/v1/dock-appointments",
        headers=bearer_auth_headers(),
        json=_payload(ships, halts),
    )
    assert response.status_code == 400
    assert "magazyn" in response.json()["detail"]


def test_http_unknown_shipment_is_404(dock_client: object) -> None:
    client, _ships, halts, _places = dock_client
    assert halts.row is not None
    response = client.post(
        "/api/v1/dock-appointments",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(uuid4()),
            "stop_id": str(halts.row.id),
            "appointment_code": "dock_9",
            "appointment_status": "noted",
            "window_date": "2026-09-09",
            "window_start_local": "08:00:00",
            "window_end_local": "10:00:00",
            "source_ref": "fixture://dock-appointment/1",
        },
    )
    assert response.status_code == 404
