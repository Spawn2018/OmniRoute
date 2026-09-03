from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.shipment_leg import require_leg_source_ref
from app.main import app
from app.models.shipment_leg import ShipmentLeg
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


class _Ship:
    def __init__(self, row_id: UUID) -> None:
        self.id = row_id


class _Loc:
    def __init__(self, row_id: UUID, kind: str) -> None:
        self.id = row_id
        self.kind = kind


class StubShipmentService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.by_id: dict[UUID, _Ship] = {}

    async def get_shipment(self, shipment_id: UUID) -> _Ship:
        found = self.by_id.get(shipment_id)
        if found is None:
            raise ResourceNotFound("nieznane zlecenie")
        return found


class StubLocationService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.by_id: dict[UUID, _Loc] = {}

    async def get_location(self, location_id: UUID) -> _Loc:
        found = self.by_id.get(location_id)
        if found is None:
            raise ResourceNotFound("nieznana lokalizacja")
        return found


class StubShipmentLegService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[ShipmentLeg] = []

    async def list_legs(self) -> list[ShipmentLeg]:
        return list(self.rows)

    async def record_leg(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: UUID,
        origin_location_id: UUID,
        destination_location_id: UUID,
        source_ref: str,
    ) -> ShipmentLeg:
        row = ShipmentLeg(
            id=uuid4(),
            organization_id=organization_id,
            shipment_id=shipment_id,
            origin_location_id=origin_location_id,
            destination_location_id=destination_location_id,
            leg_kind="road",
            source_ref=require_leg_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    ships = StubShipmentService(object())
    places = StubLocationService(object())
    rows = StubShipmentLegService(object())
    ship = _Ship(uuid4())
    origin = _Loc(uuid4(), "postal_zone")
    dest = _Loc(uuid4(), "address")
    port = _Loc(uuid4(), "unlocode")
    ships.by_id = {ship.id: ship}
    places.by_id = {origin.id: origin, dest.id: dest, port.id: port}

    def _ships(_session: object) -> StubShipmentService:
        return ships

    def _places(_session: object) -> StubLocationService:
        return places

    def _rows(_session: object) -> StubShipmentLegService:
        return rows

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.shipment_legs.ShipmentService", _ships)
    monkeypatch.setattr("app.api.shipment_legs.LocationService", _places)
    monkeypatch.setattr("app.api.shipment_legs.ShipmentLegService", _rows)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), ship, origin, dest, port
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_shipment_leg(catalog_client: object) -> None:
    client, ship, origin, dest, _port = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/shipment-legs",
        headers=headers,
        json={
            "shipment_id": str(ship.id),
            "origin_location_id": str(origin.id),
            "destination_location_id": str(dest.id),
            "source_ref": "fixture://shipment-leg/1",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["shipment_id"] == str(ship.id)
    assert body["origin_location_id"] == str(origin.id)
    assert body["destination_location_id"] == str(dest.id)
    assert body["leg_kind"] == "road"
    assert "amount" not in body
    assert "lat" not in body
    listed = client.get("/api/v1/shipment-legs", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_unknown_shipment_is_404(catalog_client: object) -> None:
    client, _ship, origin, dest, _port = catalog_client
    response = client.post(
        "/api/v1/shipment-legs",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(uuid4()),
            "origin_location_id": str(origin.id),
            "destination_location_id": str(dest.id),
            "source_ref": "fixture://shipment-leg/1",
        },
    )
    assert response.status_code == 404


def test_http_create_unknown_location_is_404(catalog_client: object) -> None:
    client, ship, origin, _dest, _port = catalog_client
    response = client.post(
        "/api/v1/shipment-legs",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ship.id),
            "origin_location_id": str(origin.id),
            "destination_location_id": str(uuid4()),
            "source_ref": "fixture://shipment-leg/1",
        },
    )
    assert response.status_code == 404


def test_http_create_unlocode_is_400(catalog_client: object) -> None:
    client, ship, origin, _dest, port = catalog_client
    response = client.post(
        "/api/v1/shipment-legs",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ship.id),
            "origin_location_id": str(origin.id),
            "destination_location_id": str(port.id),
            "source_ref": "fixture://shipment-leg/1",
        },
    )
    assert response.status_code == 400
    assert "UN/LOCODE" in response.json()["detail"]


def test_http_create_same_ends_is_400(catalog_client: object) -> None:
    client, ship, origin, _dest, _port = catalog_client
    response = client.post(
        "/api/v1/shipment-legs",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ship.id),
            "origin_location_id": str(origin.id),
            "destination_location_id": str(origin.id),
            "source_ref": "fixture://shipment-leg/1",
        },
    )
    assert response.status_code == 400
    assert "różne" in response.json()["detail"]


def test_http_create_empty_source_ref_is_400(catalog_client: object) -> None:
    client, ship, origin, dest, _port = catalog_client
    response = client.post(
        "/api/v1/shipment-legs",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ship.id),
            "origin_location_id": str(origin.id),
            "destination_location_id": str(dest.id),
            "source_ref": "   ",
        },
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]
