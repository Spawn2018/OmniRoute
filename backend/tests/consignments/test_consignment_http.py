from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.consignment import (
    require_consignment_ref,
    require_consignment_shipment_id,
    require_consignment_source_ref,
)
from app.domain.errors import ResourceNotFound
from app.main import app
from app.models.consignment import Consignment
from app.models.shipment import Shipment
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


class StubConsignmentService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[Consignment] = []

    async def list_parcels(self) -> list[Consignment]:
        return list(self.rows)

    async def record_parcel(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: object,
        consignment_ref: object,
        source_ref: object,
    ) -> Consignment:
        row = Consignment(
            id=uuid4(),
            organization_id=organization_id,
            shipment_id=require_consignment_shipment_id(shipment_id),
            consignment_ref=require_consignment_ref(consignment_ref),
            source_ref=require_consignment_source_ref(source_ref),
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


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    ships = StubShipmentService(object())
    rows = StubConsignmentService(object())

    def _ships(_session: object) -> StubShipmentService:
        return ships

    def _rows(_session: object) -> StubConsignmentService:
        return rows

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.consignments.ShipmentService", _ships)
    monkeypatch.setattr("app.api.consignments.ConsignmentService", _rows)
    ships.row = _shipment()
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), ships, rows
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_consignment(catalog_client: object) -> None:
    client, ships, _rows = catalog_client
    assert ships.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/consignments",
        headers=headers,
        json={
            "shipment_id": str(ships.row.id),
            "consignment_ref": "CN-1",
            "source_ref": "fixture://consignment/1",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["shipment_id"] == str(ships.row.id)
    assert body["consignment_ref"] == "CN-1"
    assert "amount" not in body
    listed = client.get("/api/v1/consignments", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_two_consignments_on_one_shipment(catalog_client: object) -> None:
    client, ships, _rows = catalog_client
    assert ships.row is not None
    headers = bearer_auth_headers()
    first = client.post(
        "/api/v1/consignments",
        headers=headers,
        json={
            "shipment_id": str(ships.row.id),
            "consignment_ref": "CN-1",
            "source_ref": "fixture://consignment/1",
        },
    )
    second = client.post(
        "/api/v1/consignments",
        headers=headers,
        json={
            "shipment_id": str(ships.row.id),
            "consignment_ref": "CN-2",
            "source_ref": "fixture://consignment/2",
        },
    )
    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["id"] != second.json()["id"]


def test_http_create_consignment_unknown_shipment_is_404(catalog_client: object) -> None:
    client, _ships, _rows = catalog_client
    response = client.post(
        "/api/v1/consignments",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(uuid4()),
            "consignment_ref": "CN-1",
            "source_ref": "fixture://consignment/1",
        },
    )
    assert response.status_code == 404


def test_http_create_consignment_bool_shipment_is_400(catalog_client: object) -> None:
    client, _ships, _rows = catalog_client
    response = client.post(
        "/api/v1/consignments",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": True,
            "consignment_ref": "CN-1",
            "source_ref": "fixture://consignment/1",
        },
    )
    assert response.status_code == 400
    assert "zlecenie" in response.json()["detail"]


def test_http_create_consignment_missing_shipment_is_400(catalog_client: object) -> None:
    client, _ships, _rows = catalog_client
    response = client.post(
        "/api/v1/consignments",
        headers=bearer_auth_headers(),
        json={
            "consignment_ref": "CN-1",
            "source_ref": "fixture://consignment/1",
        },
    )
    assert response.status_code == 400
    assert "zlecenie" in response.json()["detail"]


def test_http_create_consignment_bad_ref_is_400(catalog_client: object) -> None:
    client, ships, _rows = catalog_client
    assert ships.row is not None
    response = client.post(
        "/api/v1/consignments",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ships.row.id),
            "consignment_ref": "CN 1",
            "source_ref": "fixture://consignment/1",
        },
    )
    assert response.status_code == 400
    assert "przesyłka" in response.json()["detail"]


def test_http_create_consignment_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, ships, _rows = catalog_client
    assert ships.row is not None
    response = client.post(
        "/api/v1/consignments",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ships.row.id),
            "consignment_ref": "CN-1",
            "source_ref": "http://hold.example/x",
        },
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
