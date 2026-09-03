from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.collective_invoice import require_collective_source_ref
from app.domain.errors import ResourceNotFound
from app.main import app
from app.models.collective_invoice import CollectiveInvoice
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


class _Invoice:
    def __init__(self, row_id: UUID, shipment_id: UUID) -> None:
        self.id = row_id
        self.shipment_id = shipment_id


class _Ship:
    def __init__(self, row_id: UUID, party_id: UUID) -> None:
        self.id = row_id
        self.party_id = party_id


class StubSalesInvoiceService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: _Invoice | None = None

    async def get_invoice(self, invoice_id: UUID) -> _Invoice:
        if self.row is None or self.row.id != invoice_id:
            raise ResourceNotFound("nieznana faktura")
        return self.row


class StubShipmentService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.by_id: dict[UUID, _Ship] = {}

    async def get_shipment(self, shipment_id: UUID) -> _Ship:
        found = self.by_id.get(shipment_id)
        if found is None:
            raise ResourceNotFound("nieznane zlecenie")
        return found


class StubCollectiveInvoiceService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[CollectiveInvoice] = []

    async def list_members(self) -> list[CollectiveInvoice]:
        return list(self.rows)

    async def record_member(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        sales_invoice_id: UUID,
        shipment_id: UUID,
        source_ref: str,
    ) -> CollectiveInvoice:
        row = CollectiveInvoice(
            id=uuid4(),
            organization_id=organization_id,
            sales_invoice_id=sales_invoice_id,
            shipment_id=shipment_id,
            source_ref=require_collective_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    invoices = StubSalesInvoiceService(object())
    ships = StubShipmentService(object())
    rows = StubCollectiveInvoiceService(object())
    party = uuid4()
    anchor = _Ship(uuid4(), party)
    extra = _Ship(uuid4(), party)
    invoice = _Invoice(uuid4(), anchor.id)
    invoices.row = invoice
    ships.by_id = {anchor.id: anchor, extra.id: extra}

    def _invoices(_session: object) -> StubSalesInvoiceService:
        return invoices

    def _ships(_session: object) -> StubShipmentService:
        return ships

    def _rows(_session: object) -> StubCollectiveInvoiceService:
        return rows

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.collective_invoices.SalesInvoiceService", _invoices)
    monkeypatch.setattr("app.api.collective_invoices.ShipmentService", _ships)
    monkeypatch.setattr("app.api.collective_invoices.CollectiveInvoiceService", _rows)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), invoices, extra
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_collective_invoice(catalog_client: object) -> None:
    client, invoices, extra = catalog_client
    assert invoices.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/collective-invoices",
        headers=headers,
        json={
            "sales_invoice_id": str(invoices.row.id),
            "shipment_id": str(extra.id),
            "source_ref": "fixture://collective-invoice/1",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["sales_invoice_id"] == str(invoices.row.id)
    assert body["shipment_id"] == str(extra.id)
    assert "amount" not in body
    listed = client.get("/api/v1/collective-invoices", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_unknown_invoice_is_404(catalog_client: object) -> None:
    client, _invoices, extra = catalog_client
    response = client.post(
        "/api/v1/collective-invoices",
        headers=bearer_auth_headers(),
        json={
            "sales_invoice_id": str(uuid4()),
            "shipment_id": str(extra.id),
            "source_ref": "fixture://collective-invoice/1",
        },
    )
    assert response.status_code == 404


def test_http_create_anchor_shipment_is_400(catalog_client: object) -> None:
    client, invoices, _extra = catalog_client
    assert invoices.row is not None
    response = client.post(
        "/api/v1/collective-invoices",
        headers=bearer_auth_headers(),
        json={
            "sales_invoice_id": str(invoices.row.id),
            "shipment_id": str(invoices.row.shipment_id),
            "source_ref": "fixture://collective-invoice/1",
        },
    )
    assert response.status_code == 400
    assert "kotwicą" in response.json()["detail"]


def test_http_create_empty_source_ref_is_400(catalog_client: object) -> None:
    client, invoices, extra = catalog_client
    assert invoices.row is not None
    response = client.post(
        "/api/v1/collective-invoices",
        headers=bearer_auth_headers(),
        json={
            "sales_invoice_id": str(invoices.row.id),
            "shipment_id": str(extra.id),
            "source_ref": "   ",
        },
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_http_create_unknown_extra_shipment_is_404(catalog_client: object) -> None:
    client, invoices, _extra = catalog_client
    assert invoices.row is not None
    response = client.post(
        "/api/v1/collective-invoices",
        headers=bearer_auth_headers(),
        json={
            "sales_invoice_id": str(invoices.row.id),
            "shipment_id": str(uuid4()),
            "source_ref": "fixture://collective-invoice/1",
        },
    )
    assert response.status_code == 404
