from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.ocean_bill import (
    require_bill_kind,
    require_bill_no,
    require_bill_source_ref,
)
from app.main import app
from app.models.ocean_bill import OceanBill
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


class StubOceanBillService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[OceanBill] = []

    async def list_bills(self) -> list[OceanBill]:
        return list(self.rows)

    async def record_bill(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: UUID,
        bill_no: str,
        bill_kind: str,
        source_ref: str,
    ) -> OceanBill:
        row = OceanBill(
            id=uuid4(),
            organization_id=organization_id,
            shipment_id=shipment_id,
            bill_no=require_bill_no(bill_no),
            bill_kind=require_bill_kind(bill_kind),
            source_ref=require_bill_source_ref(source_ref),
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
    rows = StubOceanBillService(object())

    def _ships(_session: object) -> StubShipmentService:
        return ships

    def _rows(_session: object) -> StubOceanBillService:
        return rows

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.ocean_bills.ShipmentService", _ships)
    monkeypatch.setattr("app.api.ocean_bills.OceanBillService", _rows)
    ships.row = _shipment()
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), ships, rows
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_ocean_bill(catalog_client: object) -> None:
    client, ships, _rows = catalog_client
    assert ships.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/ocean-bills",
        headers=headers,
        json={
            "shipment_id": str(ships.row.id),
            "bill_no": "HLCUSHA1234567",
            "bill_kind": "hbl",
            "source_ref": "fixture://ocean-bill/1",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["shipment_id"] == str(ships.row.id)
    assert body["bill_no"] == "HLCUSHA1234567"
    assert body["bill_kind"] == "hbl"
    assert "amount" not in body
    assert "buy_amount" not in body
    listed = client.get("/api/v1/ocean-bills", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_ocean_bill_unknown_shipment_is_404(catalog_client: object) -> None:
    client, _ships, _rows = catalog_client
    response = client.post(
        "/api/v1/ocean-bills",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(uuid4()),
            "bill_no": "HLCUSHA1234567",
            "bill_kind": "hbl",
            "source_ref": "fixture://ocean-bill/1",
        },
    )
    assert response.status_code == 404


def test_http_create_ocean_bill_unknown_kind_is_400(catalog_client: object) -> None:
    client, ships, _rows = catalog_client
    assert ships.row is not None
    response = client.post(
        "/api/v1/ocean-bills",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ships.row.id),
            "bill_no": "HLCUSHA1234567",
            "bill_kind": "hawb",
            "source_ref": "fixture://ocean-bill/1",
        },
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_http_create_ocean_bill_empty_no_is_400(catalog_client: object) -> None:
    client, ships, _rows = catalog_client
    assert ships.row is not None
    response = client.post(
        "/api/v1/ocean-bills",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ships.row.id),
            "bill_no": "   ",
            "bill_kind": "hbl",
            "source_ref": "fixture://ocean-bill/1",
        },
    )
    assert response.status_code == 400
    assert "numer" in response.json()["detail"]


def test_http_create_ocean_bill_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, ships, _rows = catalog_client
    assert ships.row is not None
    response = client.post(
        "/api/v1/ocean-bills",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ships.row.id),
            "bill_no": "HLCUSHA1234567",
            "bill_kind": "hbl",
            "source_ref": "http://hold.example/x",
        },
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
