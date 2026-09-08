from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.shipment_package import (
    require_package_code,
    require_package_source_ref,
    require_package_status,
    require_scan_token,
)
from app.main import app
from app.models.shipment import Shipment
from app.models.shipment_package import ShipmentPackage
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


class StubShipmentPackageService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[ShipmentPackage] = []

    async def list_packages(self) -> list[ShipmentPackage]:
        return list(self.rows)

    async def record_package(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: object,
        stop_id: object,
        package_code: object,
        package_status: object,
        scan_token: object,
        source_ref: object,
    ) -> ShipmentPackage:
        code = require_package_code(package_code)
        row = ShipmentPackage(
            id=uuid4(),
            organization_id=organization_id,
            shipment_id=shipment_id if type(shipment_id) is UUID else uuid4(),
            stop_id=stop_id if type(stop_id) is UUID else uuid4(),
            package_code=code,
            package_status=require_package_status(package_status),
            scan_token=require_scan_token(scan_token, code),
            source_ref=require_package_source_ref(source_ref),
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


def _halt(shipment_id: UUID) -> Stop:
    return Stop(
        id=uuid4(),
        organization_id=uuid4(),
        shipment_id=shipment_id,
        location_id=uuid4(),
        stop_kind="loading",
        sequence_no=1,
        time_zone="Europe/Warsaw",
        status="pending",
        source_ref="fixture://stop/1",
    )


@pytest.fixture
def parcel_client(monkeypatch: pytest.MonkeyPatch) -> object:
    ships = StubShipmentService(object())
    halts = StubStopService(object())
    parcels = StubShipmentPackageService(object())
    ships.row = _shipment()
    assert ships.row is not None
    halts.row = _halt(ships.row.id)

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.shipment_packages.ShipmentService", lambda _s: ships)
    monkeypatch.setattr("app.api.shipment_packages.StopService", lambda _s: halts)
    monkeypatch.setattr("app.api.shipment_packages.ShipmentPackageService", lambda _s: parcels)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), ships, halts
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_list_and_reject_foreign_scan(parcel_client: object) -> None:
    client, ships, halts = parcel_client
    assert ships.row is not None
    assert halts.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    payload = {
        "shipment_id": str(ships.row.id),
        "stop_id": str(halts.row.id),
        "package_code": "box_1",
        "package_status": "at_stop",
        "scan_token": "omni://shipment-package/box_1",
        "source_ref": "tenant:manual",
    }
    created = client.post("/api/v1/shipment-packages", headers=headers, json=payload)
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["package_code"] == "box_1"
    assert "amount" not in body
    listed = client.get("/api/v1/shipment-packages", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]
    barcode = client.post(
        "/api/v1/shipment-packages",
        headers=headers,
        json={**payload, "package_code": "box_2", "scan_token": "ean-999"},
    )
    assert barcode.status_code == 400
    assert "QR Omni" in barcode.json()["detail"]


def test_http_unknown_shipment_is_404(parcel_client: object) -> None:
    client, _ships, halts = parcel_client
    assert halts.row is not None
    response = client.post(
        "/api/v1/shipment-packages",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(uuid4()),
            "stop_id": str(halts.row.id),
            "package_code": "box_9",
            "package_status": "noted",
            "scan_token": "omni://shipment-package/box_9",
            "source_ref": "fixture://shipment-package/1",
        },
    )
    assert response.status_code == 404


def test_http_stop_off_route_is_400(parcel_client: object) -> None:
    client, ships, halts = parcel_client
    assert ships.row is not None
    assert halts.row is not None
    halts.row.shipment_id = uuid4()
    response = client.post(
        "/api/v1/shipment-packages",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ships.row.id),
            "stop_id": str(halts.row.id),
            "package_code": "box_3",
            "package_status": "at_stop",
            "scan_token": "fixture://omni-qr/box_3",
            "source_ref": "tenant:manual",
        },
    )
    assert response.status_code == 400
    assert "trasy" in response.json()["detail"]
