from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.stop import (
    require_eta_legal,
    require_eta_physical,
    require_notes_for_driver,
    require_sequence_no,
    require_stop_appointment_ref,
    require_stop_group_code,
    require_stop_kind,
    require_stop_packaging_code,
    require_stop_pod_quality,
    require_stop_quantity,
    require_stop_seal_in,
    require_stop_seal_out,
    require_stop_source_ref,
    require_stop_status,
    require_stop_waiting_free_minutes,
    require_stop_waiting_started_at,
    require_stop_weight_kg,
    require_time_zone,
)
from app.main import app
from app.models.location import Location
from app.models.shipment import Shipment
from app.models.stop import Stop
from tests.http_auth import bearer_auth_headers

_HITL_ISO = "2026-09-09T12:00:00+00:00"


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
        eta_physical: object,
        eta_legal: object,
        stop_group_code: object = None,
        stop_group_id: object = None,
        notes_for_driver: object = None,
        weight_kg: object = None,
        quantity: object = None,
        packaging_code: object = None,
        seal_in: object = None,
        seal_out: object = None,
        appointment_ref: object = None,
        waiting_free_minutes: object = None,
        waiting_started_at: object = None,
        pod_quality: object = None,
    ) -> Stop:
        kind = require_stop_kind(stop_kind)
        seq = require_sequence_no(sequence_no)
        zone = require_time_zone(time_zone)
        state = require_stop_status(status)
        origin = require_stop_source_ref(source_ref)
        group = require_stop_group_code(stop_group_code)
        group_token = stop_group_id if type(stop_group_id) is UUID else None
        notes = require_notes_for_driver(notes_for_driver)
        mass = require_stop_weight_kg(weight_kg)
        count = require_stop_quantity(quantity)
        pack = require_stop_packaging_code(packaging_code)
        inbound = require_stop_seal_in(seal_in)
        outbound = require_stop_seal_out(seal_out)
        booking = require_stop_appointment_ref(appointment_ref)
        wait_free = require_stop_waiting_free_minutes(waiting_free_minutes)
        wait_start = require_stop_waiting_started_at(waiting_started_at)
        pod = require_stop_pod_quality(pod_quality)
        physical = require_eta_physical(eta_physical)
        legal = require_eta_legal(eta_legal)
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
            and current.eta_physical == physical
            and current.eta_legal == legal
            and current.stop_group_code == group
            and current.stop_group_id == group_token
            and current.notes_for_driver == notes
            and current.weight_kg == mass
            and current.quantity == count
            and current.packaging_code == pack
            and current.seal_in == inbound
            and current.seal_out == outbound
            and current.appointment_ref == booking
            and current.waiting_free_minutes == wait_free
            and current.waiting_started_at == wait_start
            and current.pod_quality == pod
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
            stop_group_code=group,
            stop_group_id=group_token,
            notes_for_driver=notes,
            weight_kg=mass,
            quantity=count,
            packaging_code=pack,
            seal_in=inbound,
            seal_out=outbound,
            appointment_ref=booking,
            waiting_free_minutes=wait_free,
            waiting_started_at=wait_start,
            pod_quality=pod,
            eta_physical=physical,
            eta_legal=legal,
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


class StubStopGroupService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: object | None = None

    async def get_group(self, group_id: UUID) -> object:
        from types import SimpleNamespace

        if self.row is None:
            raise ResourceNotFound("nieznana grupa punktów")
        group = self.row
        assert isinstance(group, SimpleNamespace)
        if group.id != group_id:
            raise ResourceNotFound("nieznana grupa punktów")
        return group


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    ships = StubShipmentService(object())
    places = StubLocationService(object())
    rows = StubStopService(object())
    groups = StubStopGroupService(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.stops.ShipmentService", lambda _s: ships)
    monkeypatch.setattr("app.api.stops.LocationService", lambda _s: places)
    monkeypatch.setattr("app.api.stops.StopService", lambda _s: rows)
    monkeypatch.setattr("app.api.stops.StopGroupService", lambda _s: groups)
    ships.row = _shipment()
    places.row = _place()
    rows.groups = groups
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
        "eta_physical": _HITL_ISO,
        "eta_legal": _HITL_ISO,
    }
    first = client.post("/api/v1/stops", headers=headers, json=payload)
    assert first.status_code == 201
    assert first.json()["stop_group_code"] is None
    assert first.json()["stop_group_id"] is None
    assert first.json()["notes_for_driver"] is None
    assert "amount" not in first.json()
    assert first.json()["eta_physical"].startswith("2026-09-09T12:00:00")
    assert first.json()["eta_legal"].startswith("2026-09-09T12:00:00")
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
    assert listed.json()[0]["eta_physical"].startswith("2026-09-09T12:00:00")
    pickup = client.post("/api/v1/stops", headers=headers, json={**payload, "stop_kind": "pickup"})
    assert pickup.status_code == 400
    queued = client.post("/api/v1/stops", headers=headers, json={**payload, "status": "queued"})
    assert queued.status_code == 400
    blank = client.post("/api/v1/stops", headers=headers, json={**payload, "eta_physical": ""})
    assert blank.status_code == 400
    assert "fizyczny" in blank.json()["detail"]
    naive = client.post(
        "/api/v1/stops",
        headers=headers,
        json={**payload, "eta_physical": "2026-09-09T12:00:00"},
    )
    assert naive.status_code == 400
    assert "fizyczny" in naive.json()["detail"]
    bad_legal = client.post(
        "/api/v1/stops",
        headers=headers,
        json={**payload, "eta_legal": "nie-czas"},
    )
    assert bad_legal.status_code == 400
    assert "prawny" in bad_legal.json()["detail"]


def test_http_create_stop_with_group_code(catalog_client: object) -> None:
    client, ships, places, _rows = catalog_client
    assert ships.row is not None
    assert places.row is not None
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/stops",
        headers=headers,
        json={
            "shipment_id": str(ships.row.id),
            "location_id": str(places.row.id),
            "stop_kind": "loading",
            "sequence_no": 2,
            "time_zone": "Europe/Warsaw",
            "status": "pending",
            "source_ref": "tenant:manual",
            "eta_physical": _HITL_ISO,
            "eta_legal": _HITL_ISO,
            "stop_group_code": "ZA-WY-1",
        },
    )
    assert created.status_code == 201
    assert created.json()["stop_group_code"] == "ZA-WY-1"
    assert "weight" not in created.json()
    assert "margin" not in created.json()


def test_http_rejects_loose_stop_group_code(catalog_client: object) -> None:
    client, ships, places, _rows = catalog_client
    assert ships.row is not None
    assert places.row is not None
    headers = bearer_auth_headers()
    payload = {
        "shipment_id": str(ships.row.id),
        "location_id": str(places.row.id),
        "stop_kind": "loading",
        "sequence_no": 3,
        "time_zone": "Europe/Warsaw",
        "status": "pending",
        "source_ref": "tenant:manual",
        "eta_physical": _HITL_ISO,
        "eta_legal": _HITL_ISO,
        "stop_group_code": "x",
    }
    short = client.post("/api/v1/stops", headers=headers, json=payload)
    assert short.status_code == 400
    assert "grupa" in short.json()["detail"]
    spaced = client.post(
        "/api/v1/stops",
        headers=headers,
        json={**payload, "stop_group_code": "has space"},
    )
    assert spaced.status_code == 400
    assert "grupa" in spaced.json()["detail"]


def test_http_create_stop_with_notes_for_driver(catalog_client: object) -> None:
    client, ships, places, _rows = catalog_client
    assert ships.row is not None
    assert places.row is not None
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/stops",
        headers=headers,
        json={
            "shipment_id": str(ships.row.id),
            "location_id": str(places.row.id),
            "stop_kind": "loading",
            "sequence_no": 4,
            "time_zone": "Europe/Warsaw",
            "status": "pending",
            "source_ref": "tenant:manual",
            "eta_physical": _HITL_ISO,
            "eta_legal": _HITL_ISO,
            "notes_for_driver": " brama B, dzwonek 2 ",
        },
    )
    assert created.status_code == 201
    assert created.json()["notes_for_driver"] == "brama B, dzwonek 2"
    assert created.json()["weight_kg"] is None
    assert created.json()["quantity"] is None
    assert created.json()["packaging_code"] is None
    assert created.json()["seal_in"] is None
    assert created.json()["seal_out"] is None
    assert created.json()["appointment_ref"] is None
    assert created.json()["waiting_free_minutes"] is None
    assert created.json()["waiting_started_at"] is None
    assert created.json()["pod_quality"] is None
    assert "margin" not in created.json()


def test_http_rejects_too_long_notes_for_driver(catalog_client: object) -> None:
    client, ships, places, _rows = catalog_client
    assert ships.row is not None
    assert places.row is not None
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/stops",
        headers=headers,
        json={
            "shipment_id": str(ships.row.id),
            "location_id": str(places.row.id),
            "stop_kind": "loading",
            "sequence_no": 5,
            "time_zone": "Europe/Warsaw",
            "status": "pending",
            "source_ref": "tenant:manual",
            "eta_physical": _HITL_ISO,
            "eta_legal": _HITL_ISO,
            "notes_for_driver": "x" * 257,
        },
    )
    assert reply.status_code == 400
    assert "notatka" in reply.json()["detail"]


def test_http_create_stop_with_weight_kg(catalog_client: object) -> None:
    client, ships, places, _rows = catalog_client
    assert ships.row is not None
    assert places.row is not None
    created = client.post(
        "/api/v1/stops",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ships.row.id),
            "location_id": str(places.row.id),
            "stop_kind": "loading",
            "sequence_no": 6,
            "time_zone": "Europe/Warsaw",
            "status": "pending",
            "source_ref": "tenant:manual",
            "eta_physical": _HITL_ISO,
            "eta_legal": _HITL_ISO,
            "weight_kg": "12.5",
        },
    )
    assert created.status_code == 201
    assert created.json()["weight_kg"] == "12.5000"
    assert created.json()["quantity"] is None
    assert "margin" not in created.json()


def test_http_rejects_float_and_negative_weight_kg(catalog_client: object) -> None:
    client, ships, places, _rows = catalog_client
    assert ships.row is not None
    assert places.row is not None
    headers = bearer_auth_headers()
    payload = {
        "shipment_id": str(ships.row.id),
        "location_id": str(places.row.id),
        "stop_kind": "loading",
        "sequence_no": 7,
        "time_zone": "Europe/Warsaw",
        "status": "pending",
        "source_ref": "tenant:manual",
        "eta_physical": _HITL_ISO,
        "eta_legal": _HITL_ISO,
        "weight_kg": "-1",
    }
    negative = client.post("/api/v1/stops", headers=headers, json=payload)
    assert negative.status_code == 400
    assert "waga" in negative.json()["detail"]


def test_http_create_stop_with_quantity(catalog_client: object) -> None:
    client, ships, places, _rows = catalog_client
    assert ships.row is not None
    assert places.row is not None
    created = client.post(
        "/api/v1/stops",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ships.row.id),
            "location_id": str(places.row.id),
            "stop_kind": "loading",
            "sequence_no": 8,
            "time_zone": "Europe/Warsaw",
            "status": "pending",
            "source_ref": "tenant:manual",
            "eta_physical": _HITL_ISO,
            "eta_legal": _HITL_ISO,
            "quantity": 12,
        },
    )
    assert created.status_code == 201
    assert created.json()["quantity"] == 12
    assert created.json()["weight_kg"] is None
    assert created.json()["packaging_code"] is None
    assert "margin" not in created.json()


def test_http_rejects_float_and_negative_quantity(catalog_client: object) -> None:
    client, ships, places, _rows = catalog_client
    assert ships.row is not None
    assert places.row is not None
    headers = bearer_auth_headers()
    payload = {
        "shipment_id": str(ships.row.id),
        "location_id": str(places.row.id),
        "stop_kind": "loading",
        "sequence_no": 9,
        "time_zone": "Europe/Warsaw",
        "status": "pending",
        "source_ref": "tenant:manual",
        "eta_physical": _HITL_ISO,
        "eta_legal": _HITL_ISO,
        "quantity": -1,
    }
    negative = client.post("/api/v1/stops", headers=headers, json=payload)
    assert negative.status_code == 400
    assert "ilość" in negative.json()["detail"]
    payload["quantity"] = 1.5
    floated = client.post("/api/v1/stops", headers=headers, json=payload)
    assert floated.status_code == 400
    assert "ilość" in floated.json()["detail"]


def test_http_create_stop_with_packaging_code(catalog_client: object) -> None:
    client, ships, places, _rows = catalog_client
    assert ships.row is not None
    assert places.row is not None
    created = client.post(
        "/api/v1/stops",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ships.row.id),
            "location_id": str(places.row.id),
            "stop_kind": "loading",
            "sequence_no": 10,
            "time_zone": "Europe/Warsaw",
            "status": "pending",
            "source_ref": "tenant:manual",
            "eta_physical": _HITL_ISO,
            "eta_legal": _HITL_ISO,
            "packaging_code": " EUR ",
        },
    )
    assert created.status_code == 201
    assert created.json()["packaging_code"] == "EUR"
    assert created.json()["quantity"] is None
    assert created.json()["seal_in"] is None
    assert "margin" not in created.json()


def test_http_rejects_too_long_packaging_code(catalog_client: object) -> None:
    client, ships, places, _rows = catalog_client
    assert ships.row is not None
    assert places.row is not None
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/stops",
        headers=headers,
        json={
            "shipment_id": str(ships.row.id),
            "location_id": str(places.row.id),
            "stop_kind": "loading",
            "sequence_no": 11,
            "time_zone": "Europe/Warsaw",
            "status": "pending",
            "source_ref": "tenant:manual",
            "eta_physical": _HITL_ISO,
            "eta_legal": _HITL_ISO,
            "packaging_code": "x" * 33,
        },
    )
    assert reply.status_code == 400
    assert "opakowanie" in reply.json()["detail"]


def test_http_create_stop_with_seal_in(catalog_client: object) -> None:
    client, ships, places, _rows = catalog_client
    assert ships.row is not None
    assert places.row is not None
    created = client.post(
        "/api/v1/stops",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ships.row.id),
            "location_id": str(places.row.id),
            "stop_kind": "loading",
            "sequence_no": 12,
            "time_zone": "Europe/Warsaw",
            "status": "pending",
            "source_ref": "tenant:manual",
            "eta_physical": _HITL_ISO,
            "eta_legal": _HITL_ISO,
            "seal_in": " ABC123 ",
        },
    )
    assert created.status_code == 201
    assert created.json()["seal_in"] == "ABC123"
    assert created.json()["seal_out"] is None
    assert "margin" not in created.json()


def test_http_rejects_too_long_seal_in(catalog_client: object) -> None:
    client, ships, places, _rows = catalog_client
    assert ships.row is not None
    assert places.row is not None
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/stops",
        headers=headers,
        json={
            "shipment_id": str(ships.row.id),
            "location_id": str(places.row.id),
            "stop_kind": "loading",
            "sequence_no": 13,
            "time_zone": "Europe/Warsaw",
            "status": "pending",
            "source_ref": "tenant:manual",
            "eta_physical": _HITL_ISO,
            "eta_legal": _HITL_ISO,
            "seal_in": "x" * 33,
        },
    )
    assert reply.status_code == 400
    assert "plomba" in reply.json()["detail"]


def test_http_create_stop_with_seal_out(catalog_client: object) -> None:
    client, ships, places, _rows = catalog_client
    assert ships.row is not None
    assert places.row is not None
    created = client.post(
        "/api/v1/stops",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ships.row.id),
            "location_id": str(places.row.id),
            "stop_kind": "loading",
            "sequence_no": 14,
            "time_zone": "Europe/Warsaw",
            "status": "pending",
            "source_ref": "tenant:manual",
            "eta_physical": _HITL_ISO,
            "eta_legal": _HITL_ISO,
            "seal_out": " XYZ ",
        },
    )
    assert created.status_code == 201
    assert created.json()["seal_out"] == "XYZ"
    assert created.json()["seal_in"] is None
    assert created.json()["appointment_ref"] is None
    assert "margin" not in created.json()


def test_http_rejects_too_long_seal_out(catalog_client: object) -> None:
    client, ships, places, _rows = catalog_client
    assert ships.row is not None
    assert places.row is not None
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/stops",
        headers=headers,
        json={
            "shipment_id": str(ships.row.id),
            "location_id": str(places.row.id),
            "stop_kind": "loading",
            "sequence_no": 15,
            "time_zone": "Europe/Warsaw",
            "status": "pending",
            "source_ref": "tenant:manual",
            "eta_physical": _HITL_ISO,
            "eta_legal": _HITL_ISO,
            "seal_out": "x" * 33,
        },
    )
    assert reply.status_code == 400
    assert "plomba" in reply.json()["detail"]


def test_http_create_stop_with_appointment_ref(catalog_client: object) -> None:
    client, ships, places, _rows = catalog_client
    assert ships.row is not None
    assert places.row is not None
    created = client.post(
        "/api/v1/stops",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ships.row.id),
            "location_id": str(places.row.id),
            "stop_kind": "loading",
            "sequence_no": 16,
            "time_zone": "Europe/Warsaw",
            "status": "pending",
            "source_ref": "tenant:manual",
            "eta_physical": _HITL_ISO,
            "eta_legal": _HITL_ISO,
            "appointment_ref": " WH-12 ",
        },
    )
    assert created.status_code == 201
    assert created.json()["appointment_ref"] == "WH-12"
    assert created.json()["seal_out"] is None
    assert "margin" not in created.json()


def test_http_rejects_too_long_appointment_ref(catalog_client: object) -> None:
    client, ships, places, _rows = catalog_client
    assert ships.row is not None
    assert places.row is not None
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/stops",
        headers=headers,
        json={
            "shipment_id": str(ships.row.id),
            "location_id": str(places.row.id),
            "stop_kind": "loading",
            "sequence_no": 17,
            "time_zone": "Europe/Warsaw",
            "status": "pending",
            "source_ref": "tenant:manual",
            "eta_physical": _HITL_ISO,
            "eta_legal": _HITL_ISO,
            "appointment_ref": "x" * 33,
        },
    )
    assert reply.status_code == 400
    assert "awizacja" in reply.json()["detail"]


def test_http_create_stop_with_waiting_free_minutes(catalog_client: object) -> None:
    client, ships, places, _rows = catalog_client
    assert ships.row is not None
    assert places.row is not None
    created = client.post(
        "/api/v1/stops",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ships.row.id),
            "location_id": str(places.row.id),
            "stop_kind": "loading",
            "sequence_no": 18,
            "time_zone": "Europe/Warsaw",
            "status": "pending",
            "source_ref": "tenant:manual",
            "eta_physical": _HITL_ISO,
            "eta_legal": _HITL_ISO,
            "waiting_free_minutes": 15,
        },
    )
    assert created.status_code == 201
    assert created.json()["waiting_free_minutes"] == 15
    assert created.json()["appointment_ref"] is None
    assert "margin" not in created.json()


def test_http_rejects_float_and_negative_waiting_free(catalog_client: object) -> None:
    client, ships, places, _rows = catalog_client
    assert ships.row is not None
    assert places.row is not None
    headers = bearer_auth_headers()
    payload = {
        "shipment_id": str(ships.row.id),
        "location_id": str(places.row.id),
        "stop_kind": "loading",
        "sequence_no": 19,
        "time_zone": "Europe/Warsaw",
        "status": "pending",
        "source_ref": "tenant:manual",
        "eta_physical": _HITL_ISO,
        "eta_legal": _HITL_ISO,
        "waiting_free_minutes": -1,
    }
    negative = client.post("/api/v1/stops", headers=headers, json=payload)
    assert negative.status_code == 400
    assert "oczekiwanie" in negative.json()["detail"]
    payload["waiting_free_minutes"] = 1.5
    floated = client.post("/api/v1/stops", headers=headers, json=payload)
    assert floated.status_code == 400
    assert "oczekiwanie" in floated.json()["detail"]


def test_http_create_stop_with_waiting_started_at(catalog_client: object) -> None:
    client, ships, places, _rows = catalog_client
    assert ships.row is not None
    assert places.row is not None
    created = client.post(
        "/api/v1/stops",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ships.row.id),
            "location_id": str(places.row.id),
            "stop_kind": "loading",
            "sequence_no": 20,
            "time_zone": "Europe/Warsaw",
            "status": "pending",
            "source_ref": "tenant:manual",
            "eta_physical": _HITL_ISO,
            "eta_legal": _HITL_ISO,
            "waiting_started_at": _HITL_ISO,
        },
    )
    assert created.status_code == 201
    assert created.json()["waiting_started_at"] is not None
    assert created.json()["waiting_free_minutes"] is None
    assert "margin" not in created.json()


def test_http_rejects_naive_waiting_started_at(catalog_client: object) -> None:
    client, ships, places, _rows = catalog_client
    assert ships.row is not None
    assert places.row is not None
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/stops",
        headers=headers,
        json={
            "shipment_id": str(ships.row.id),
            "location_id": str(places.row.id),
            "stop_kind": "loading",
            "sequence_no": 21,
            "time_zone": "Europe/Warsaw",
            "status": "pending",
            "source_ref": "tenant:manual",
            "eta_physical": _HITL_ISO,
            "eta_legal": _HITL_ISO,
            "waiting_started_at": "2026-09-09T12:00:00",
        },
    )
    assert reply.status_code == 400
    assert "początek" in reply.json()["detail"]


def test_http_create_stop_with_pod_quality(catalog_client: object) -> None:
    client, ships, places, _rows = catalog_client
    assert ships.row is not None
    assert places.row is not None
    created = client.post(
        "/api/v1/stops",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ships.row.id),
            "location_id": str(places.row.id),
            "stop_kind": "loading",
            "sequence_no": 22,
            "time_zone": "Europe/Warsaw",
            "status": "pending",
            "source_ref": "tenant:manual",
            "eta_physical": _HITL_ISO,
            "eta_legal": _HITL_ISO,
            "pod_quality": "ok",
        },
    )
    assert created.status_code == 201
    assert created.json()["pod_quality"] == "ok"
    assert created.json()["waiting_started_at"] is None
    assert "margin" not in created.json()


def test_http_rejects_unknown_pod_quality(catalog_client: object) -> None:
    client, ships, places, _rows = catalog_client
    assert ships.row is not None
    assert places.row is not None
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/stops",
        headers=headers,
        json={
            "shipment_id": str(ships.row.id),
            "location_id": str(places.row.id),
            "stop_kind": "loading",
            "sequence_no": 23,
            "time_zone": "Europe/Warsaw",
            "status": "pending",
            "source_ref": "tenant:manual",
            "eta_physical": _HITL_ISO,
            "eta_legal": _HITL_ISO,
            "pod_quality": "blurry",
        },
    )
    assert reply.status_code == 400
    assert "pod" in reply.json()["detail"]


def test_http_create_stop_with_stop_group_id(catalog_client: object) -> None:
    client, ships, places, rows = catalog_client
    assert ships.row is not None
    assert places.row is not None
    group_id = uuid4()
    rows.groups.row = SimpleNamespace(id=group_id, shipment_id=ships.row.id, group_code="GRP-A")
    headers = bearer_auth_headers()
    created = client.post(
        "/api/v1/stops",
        headers=headers,
        json={
            "shipment_id": str(ships.row.id),
            "location_id": str(places.row.id),
            "stop_kind": "loading",
            "sequence_no": 24,
            "time_zone": "Europe/Warsaw",
            "status": "pending",
            "source_ref": "tenant:manual",
            "eta_physical": _HITL_ISO,
            "eta_legal": _HITL_ISO,
            "stop_group_id": str(group_id),
        },
    )
    assert created.status_code == 201
    assert created.json()["stop_group_id"] == str(group_id)
    assert created.json()["stop_group_code"] == "GRP-A"


def test_http_rejects_stop_group_code_mismatch(catalog_client: object) -> None:
    client, ships, places, rows = catalog_client
    assert ships.row is not None
    assert places.row is not None
    group_id = uuid4()
    rows.groups.row = SimpleNamespace(id=group_id, shipment_id=ships.row.id, group_code="GRP-A")
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/stops",
        headers=headers,
        json={
            "shipment_id": str(ships.row.id),
            "location_id": str(places.row.id),
            "stop_kind": "loading",
            "sequence_no": 27,
            "time_zone": "Europe/Warsaw",
            "status": "pending",
            "source_ref": "tenant:manual",
            "eta_physical": _HITL_ISO,
            "eta_legal": _HITL_ISO,
            "stop_group_id": str(group_id),
            "stop_group_code": "OTHER",
        },
    )
    assert reply.status_code == 400
    assert "grupa" in reply.json()["detail"]


def test_http_rejects_stop_group_other_shipment(catalog_client: object) -> None:
    client, ships, places, rows = catalog_client
    assert ships.row is not None
    assert places.row is not None
    group_id = uuid4()
    rows.groups.row = SimpleNamespace(id=group_id, shipment_id=uuid4())
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/stops",
        headers=headers,
        json={
            "shipment_id": str(ships.row.id),
            "location_id": str(places.row.id),
            "stop_kind": "loading",
            "sequence_no": 25,
            "time_zone": "Europe/Warsaw",
            "status": "pending",
            "source_ref": "tenant:manual",
            "eta_physical": _HITL_ISO,
            "eta_legal": _HITL_ISO,
            "stop_group_id": str(group_id),
        },
    )
    assert reply.status_code == 400
    assert "grupa" in reply.json()["detail"]


def test_http_rejects_unknown_stop_group_id(catalog_client: object) -> None:
    client, ships, places, rows = catalog_client
    assert ships.row is not None
    assert places.row is not None
    rows.groups.row = None
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/stops",
        headers=headers,
        json={
            "shipment_id": str(ships.row.id),
            "location_id": str(places.row.id),
            "stop_kind": "loading",
            "sequence_no": 26,
            "time_zone": "Europe/Warsaw",
            "status": "pending",
            "source_ref": "tenant:manual",
            "eta_physical": _HITL_ISO,
            "eta_legal": _HITL_ISO,
            "stop_group_id": str(uuid4()),
        },
    )
    assert reply.status_code == 404
