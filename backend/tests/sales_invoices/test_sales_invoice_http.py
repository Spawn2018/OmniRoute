from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.sales_invoice import (
    require_invoice_kind,
    require_invoice_ref,
    require_invoice_source_ref,
)
from app.main import app
from app.models.sales_invoice import SalesInvoice
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


class StubSalesInvoiceService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[SalesInvoice] = []

    async def list_invoices(self) -> list[SalesInvoice]:
        return list(self.rows)

    async def record_invoice(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: UUID,
        invoice_kind: str,
        invoice_ref: str,
        source_ref: str,
    ) -> SalesInvoice:
        row = SalesInvoice(
            id=uuid4(),
            organization_id=organization_id,
            shipment_id=shipment_id,
            invoice_kind=require_invoice_kind(invoice_kind),
            invoice_ref=require_invoice_ref(invoice_ref),
            source_ref=require_invoice_source_ref(source_ref),
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
    invoices = StubSalesInvoiceService(object())

    def _ships(_session: object) -> StubShipmentService:
        return ships

    def _invoices(_session: object) -> StubSalesInvoiceService:
        return invoices

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.sales_invoices.ShipmentService", _ships)
    monkeypatch.setattr("app.api.sales_invoices.SalesInvoiceService", _invoices)
    ships.row = _shipment()
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), ships, invoices
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_sales_invoice(catalog_client: object) -> None:
    client, ships, _invoices = catalog_client
    assert ships.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/sales-invoices",
        headers=headers,
        json={
            "shipment_id": str(ships.row.id),
            "invoice_kind": "issued",
            "invoice_ref": "FV/2026/1",
            "source_ref": "fixture://sales-invoice/1",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["shipment_id"] == str(ships.row.id)
    assert body["invoice_kind"] == "issued"
    assert body["invoice_ref"] == "FV/2026/1"
    assert body["source_ref"] == "fixture://sales-invoice/1"
    assert "amount" not in body
    assert "sell_amount" not in body
    assert "ksef" not in body

    listed = client.get("/api/v1/sales-invoices", headers=headers)
    assert listed.status_code == 200
    rows = listed.json()
    assert len(rows) == 1
    assert rows[0]["id"] == body["id"]


def test_http_create_sales_invoice_unknown_shipment_is_404(catalog_client: object) -> None:
    client, _ships, _invoices = catalog_client
    response = client.post(
        "/api/v1/sales-invoices",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(uuid4()),
            "invoice_kind": "issued",
            "invoice_ref": "FV/2026/1",
            "source_ref": "fixture://sales-invoice/1",
        },
    )
    assert response.status_code == 404


def test_http_create_sales_invoice_unknown_kind_is_400(catalog_client: object) -> None:
    client, ships, _invoices = catalog_client
    assert ships.row is not None
    response = client.post(
        "/api/v1/sales-invoices",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ships.row.id),
            "invoice_kind": "hold",
            "invoice_ref": "FV/2026/1",
            "source_ref": "fixture://sales-invoice/1",
        },
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_http_create_sales_invoice_empty_invoice_ref_is_400(catalog_client: object) -> None:
    client, ships, _invoices = catalog_client
    assert ships.row is not None
    response = client.post(
        "/api/v1/sales-invoices",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ships.row.id),
            "invoice_kind": "issued",
            "invoice_ref": "   ",
            "source_ref": "fixture://sales-invoice/1",
        },
    )
    assert response.status_code == 400
    assert "numer" in response.json()["detail"]


def test_http_create_sales_invoice_empty_source_ref_is_400(catalog_client: object) -> None:
    client, ships, _invoices = catalog_client
    assert ships.row is not None
    response = client.post(
        "/api/v1/sales-invoices",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ships.row.id),
            "invoice_kind": "issued",
            "invoice_ref": "FV/2026/1",
            "source_ref": "   ",
        },
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]
