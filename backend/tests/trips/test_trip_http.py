from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.trip import (
    require_distinct_drivers,
    require_expected_buy,
    require_route_label,
    require_trip_no,
    require_trip_planned_distance_km,
    require_trip_resource_id,
    require_trip_source_ref,
    require_trip_status,
)
from app.main import app
from app.models.resource import Resource
from app.models.trip import Trip
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


class StubResourceService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[Resource] = []

    async def get_resource(self, resource_id: UUID) -> Resource:
        for row in self.rows:
            if row.id == resource_id:
                return row
        raise ResourceNotFound("nieznany zasób")


class StubTripService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[Trip] = []

    async def list_trips(self, *, status: object | None = None) -> list[Trip]:
        state = None if status is None else require_trip_status(status)
        return [
            row
            for row in self.rows
            if row.superseded_by is None and (state is None or row.status == state)
        ]

    async def record_trip(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        trip_no: object,
        status: object,
        vehicle_id: object,
        trailer_id: object,
        driver_id: object,
        source_ref: object,
        expected_buy_amount: object = None,
        expected_buy_currency: object = None,
        driver2_id: object = None,
        route_label: object = None,
        planned_distance_km: object = None,
    ) -> Trip:
        number = require_trip_no(trip_no)
        state = require_trip_status(status)
        vehicle = require_trip_resource_id(vehicle_id)
        trailer = require_trip_resource_id(trailer_id)
        driver = require_trip_resource_id(driver_id)
        driver2 = require_trip_resource_id(driver2_id)
        require_distinct_drivers(driver, driver2)
        origin = require_trip_source_ref(source_ref)
        label = require_route_label(route_label)
        planned = require_trip_planned_distance_km(planned_distance_km)
        buy_amount, buy_currency = require_expected_buy(
            state,
            expected_buy_amount,
            expected_buy_currency,
        )
        current = next(
            (row for row in self.rows if row.trip_no == number and row.superseded_by is None),
            None,
        )
        if (
            current is not None
            and current.status == state
            and current.vehicle_id == vehicle
            and current.trailer_id == trailer
            and current.driver_id == driver
            and current.driver2_id == driver2
            and current.source_ref == origin
            and current.route_label == label
            and current.planned_distance_km == planned
            and current.expected_buy_amount == buy_amount
            and current.expected_buy_currency == buy_currency
        ):
            return current
        successor = Trip(
            id=uuid4(),
            organization_id=organization_id,
            trip_no=number,
            status=state,
            vehicle_id=vehicle,
            trailer_id=trailer,
            driver_id=driver,
            driver2_id=driver2,
            source_ref=origin,
            route_label=label,
            planned_distance_km=planned,
            expected_buy_amount=buy_amount,
            expected_buy_currency=buy_currency,
            created_by=user_id,
        )
        if current is not None:
            current.superseded_by = successor.id
        self.rows.append(successor)
        return successor


@pytest.fixture
def run_client(monkeypatch: pytest.MonkeyPatch) -> object:
    trips = StubTripService(object())
    fleet = StubResourceService(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.trips.TripService", lambda _s: trips)
    monkeypatch.setattr("app.api.trips.ResourceService", lambda _s: fleet)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), trips, fleet
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_list_supersede_and_reject_queued(run_client: object) -> None:
    client, _trips, _fleet = run_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    payload = {
        "trip_no": "TR-1",
        "status": "draft",
        "source_ref": "tenant:manual",
    }
    first = client.post("/api/v1/trips", headers=headers, json=payload)
    assert first.status_code == 201
    assert first.json()["organization_id"] == str(org_id)
    assert first.json()["driver2_id"] is None
    assert first.json()["route_label"] is None
    assert first.json()["planned_distance_km"] is None
    assert "amount" not in first.json()
    second = client.post(
        "/api/v1/trips",
        headers=headers,
        json={**payload, "status": "planned"},
    )
    assert second.status_code == 201
    assert second.json()["id"] != first.json()["id"]
    listed = client.get("/api/v1/trips", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == second.json()["id"]
    drafts = client.get("/api/v1/trips", headers=headers, params={"status": "draft"})
    assert drafts.json() == []
    queued = client.post(
        "/api/v1/trips",
        headers=headers,
        json={**payload, "status": "queued"},
    )
    assert queued.status_code == 400
    assert "status" in queued.json()["detail"]


def test_http_freezes_expected_buy_on_in_transit(run_client: object) -> None:
    client, _trips, _fleet = run_client
    headers = bearer_auth_headers(organization_id=uuid4())
    missing = client.post(
        "/api/v1/trips",
        headers=headers,
        json={"trip_no": "TR-3", "status": "in_transit", "source_ref": "tenant:manual"},
    )
    assert missing.status_code == 400
    assert "kwota" in missing.json()["detail"]
    early = client.post(
        "/api/v1/trips",
        headers=headers,
        json={
            "trip_no": "TR-3",
            "status": "planned",
            "expected_buy_amount": "10.0000",
            "expected_buy_currency": "EUR",
            "source_ref": "tenant:manual",
        },
    )
    assert early.status_code == 400
    assert "snapshot" in early.json()["detail"]
    frozen = client.post(
        "/api/v1/trips",
        headers=headers,
        json={
            "trip_no": "TR-3",
            "status": "in_transit",
            "expected_buy_amount": "1250.5000",
            "expected_buy_currency": "EUR",
            "source_ref": "tenant:manual",
        },
    )
    assert frozen.status_code == 201
    body = frozen.json()
    assert body["expected_buy_amount"] == "1250.5000"
    assert body["expected_buy_currency"] == "EUR"
    listed = client.get("/api/v1/trips", headers=headers, params={"status": "in_transit"})
    assert listed.json()[0]["expected_buy_amount"] == "1250.5000"


def test_http_rejects_driver_on_vehicle_slot(run_client: object) -> None:
    client, _trips, fleet = run_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    driver = Resource(
        id=uuid4(),
        organization_id=org_id,
        resource_kind="driver",
        display_name="Kowalski",
        registration_no=None,
        source_ref="fixture://resource/d",
        created_by=uuid4(),
    )
    fleet.rows.append(driver)
    reply = client.post(
        "/api/v1/trips",
        headers=headers,
        json={
            "trip_no": "TR-2",
            "status": "draft",
            "vehicle_id": str(driver.id),
            "source_ref": "tenant:manual",
        },
    )
    assert reply.status_code == 400
    assert "rodzaj" in reply.json()["detail"]


def test_http_create_trip_with_second_driver(run_client: object) -> None:
    client, _trips, fleet = run_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    first = Resource(
        id=uuid4(),
        organization_id=org_id,
        resource_kind="driver",
        display_name="Kowalski",
        registration_no=None,
        source_ref="fixture://resource/d1",
        created_by=uuid4(),
    )
    second = Resource(
        id=uuid4(),
        organization_id=org_id,
        resource_kind="driver",
        display_name="Nowak",
        registration_no=None,
        source_ref="fixture://resource/d2",
        created_by=uuid4(),
    )
    fleet.rows.extend([first, second])
    reply = client.post(
        "/api/v1/trips",
        headers=headers,
        json={
            "trip_no": "TR-4",
            "status": "draft",
            "driver_id": str(first.id),
            "driver2_id": str(second.id),
            "source_ref": "tenant:manual",
        },
    )
    assert reply.status_code == 201
    body = reply.json()
    assert body["driver_id"] == str(first.id)
    assert body["driver2_id"] == str(second.id)
    assert "km" not in body
    assert "margin" not in body


def test_http_rejects_same_uuid_on_both_driver_seats(run_client: object) -> None:
    client, _trips, fleet = run_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    driver = Resource(
        id=uuid4(),
        organization_id=org_id,
        resource_kind="driver",
        display_name="Kowalski",
        registration_no=None,
        source_ref="fixture://resource/d",
        created_by=uuid4(),
    )
    fleet.rows.append(driver)
    reply = client.post(
        "/api/v1/trips",
        headers=headers,
        json={
            "trip_no": "TR-5",
            "status": "draft",
            "driver_id": str(driver.id),
            "driver2_id": str(driver.id),
            "source_ref": "tenant:manual",
        },
    )
    assert reply.status_code == 400
    assert "kierowca" in reply.json()["detail"]


def test_http_rejects_vehicle_on_driver2_slot(run_client: object) -> None:
    client, _trips, fleet = run_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    truck = Resource(
        id=uuid4(),
        organization_id=org_id,
        resource_kind="vehicle",
        display_name="MAN",
        registration_no=None,
        source_ref="fixture://resource/v",
        created_by=uuid4(),
    )
    fleet.rows.append(truck)
    reply = client.post(
        "/api/v1/trips",
        headers=headers,
        json={
            "trip_no": "TR-6",
            "status": "draft",
            "driver2_id": str(truck.id),
            "source_ref": "tenant:manual",
        },
    )
    assert reply.status_code == 400
    assert "rodzaj" in reply.json()["detail"]


def test_http_create_trip_with_route_label(run_client: object) -> None:
    client, _trips, _fleet = run_client
    headers = bearer_auth_headers(organization_id=uuid4())
    reply = client.post(
        "/api/v1/trips",
        headers=headers,
        json={
            "trip_no": "TR-7",
            "status": "draft",
            "source_ref": "tenant:manual",
            "route_label": "GDYNIA (PL) - BLONIE (PL)",
        },
    )
    assert reply.status_code == 201
    assert reply.json()["route_label"] == "GDYNIA (PL) - BLONIE (PL)"
    assert reply.json()["planned_distance_km"] is None
    assert "margin" not in reply.json()


def test_http_rejects_too_long_route_label(run_client: object) -> None:
    client, _trips, _fleet = run_client
    headers = bearer_auth_headers(organization_id=uuid4())
    reply = client.post(
        "/api/v1/trips",
        headers=headers,
        json={
            "trip_no": "TR-8",
            "status": "draft",
            "source_ref": "tenant:manual",
            "route_label": "x" * 129,
        },
    )
    assert reply.status_code == 400
    assert "trasa" in reply.json()["detail"]


def test_http_create_trip_with_planned_distance(run_client: object) -> None:
    client, _trips, _fleet = run_client
    headers = bearer_auth_headers(organization_id=uuid4())
    reply = client.post(
        "/api/v1/trips",
        headers=headers,
        json={
            "trip_no": "TR-9",
            "status": "draft",
            "source_ref": "tenant:manual",
            "planned_distance_km": "12.5",
        },
    )
    assert reply.status_code == 201
    assert reply.json()["planned_distance_km"] == "12.5000"
    assert reply.json()["route_label"] is None
    assert "margin" not in reply.json()


def test_http_rejects_float_planned_distance(run_client: object) -> None:
    client, _trips, _fleet = run_client
    headers = bearer_auth_headers(organization_id=uuid4())
    reply = client.post(
        "/api/v1/trips",
        headers=headers,
        json={
            "trip_no": "TR-10",
            "status": "draft",
            "source_ref": "tenant:manual",
            "planned_distance_km": 1.5,
        },
    )
    assert reply.status_code == 400
    assert "km" in reply.json()["detail"]
