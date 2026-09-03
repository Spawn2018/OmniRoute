from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.bookkeeping import require_bookkeeping_source_ref
from app.domain.errors import ResourceNotFound
from app.main import app
from app.models.bookkeeping import Bookkeeping
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


class _Row:
    def __init__(self, row_id: UUID) -> None:
        self.id = row_id


class StubChargeService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: _Row | None = None

    async def get_charge(self, charge_id: UUID) -> _Row:
        if self.row is None or self.row.id != charge_id:
            raise ResourceNotFound("nieznana opłata")
        return self.row


class StubSalesInvoiceService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: _Row | None = None

    async def get_invoice(self, invoice_id: UUID) -> _Row:
        if self.row is None or self.row.id != invoice_id:
            raise ResourceNotFound("nieznana faktura")
        return self.row


class StubBookkeepingService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[Bookkeeping] = []

    async def list_entries(self) -> list[Bookkeeping]:
        return list(self.rows)

    async def record_entry(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        charge_id: UUID,
        sales_invoice_id: UUID,
        source_ref: str,
    ) -> Bookkeeping:
        row = Bookkeeping(
            id=uuid4(),
            organization_id=organization_id,
            charge_id=charge_id,
            sales_invoice_id=sales_invoice_id,
            source_ref=require_bookkeeping_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    charges = StubChargeService(object())
    invoices = StubSalesInvoiceService(object())
    rows = StubBookkeepingService(object())

    def _charges(_session: object) -> StubChargeService:
        return charges

    def _invoices(_session: object) -> StubSalesInvoiceService:
        return invoices

    def _rows(_session: object) -> StubBookkeepingService:
        return rows

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.bookkeeping.ChargeService", _charges)
    monkeypatch.setattr("app.api.bookkeeping.SalesInvoiceService", _invoices)
    monkeypatch.setattr("app.api.bookkeeping.BookkeepingService", _rows)
    charges.row = _Row(uuid4())
    invoices.row = _Row(uuid4())
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), charges, invoices
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_bookkeeping(catalog_client: object) -> None:
    client, charges, invoices = catalog_client
    assert charges.row is not None
    assert invoices.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/bookkeepings",
        headers=headers,
        json={
            "charge_id": str(charges.row.id),
            "sales_invoice_id": str(invoices.row.id),
            "source_ref": "fixture://bookkeeping/1",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["charge_id"] == str(charges.row.id)
    assert body["sales_invoice_id"] == str(invoices.row.id)
    assert "amount" not in body
    assert "buy_amount" not in body
    assert "sell_amount" not in body
    listed = client.get("/api/v1/bookkeepings", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_unknown_charge_is_404(catalog_client: object) -> None:
    client, _charges, invoices = catalog_client
    assert invoices.row is not None
    response = client.post(
        "/api/v1/bookkeepings",
        headers=bearer_auth_headers(),
        json={
            "charge_id": str(uuid4()),
            "sales_invoice_id": str(invoices.row.id),
            "source_ref": "fixture://bookkeeping/1",
        },
    )
    assert response.status_code == 404


def test_http_create_unknown_invoice_is_404(catalog_client: object) -> None:
    client, charges, _invoices = catalog_client
    assert charges.row is not None
    response = client.post(
        "/api/v1/bookkeepings",
        headers=bearer_auth_headers(),
        json={
            "charge_id": str(charges.row.id),
            "sales_invoice_id": str(uuid4()),
            "source_ref": "fixture://bookkeeping/1",
        },
    )
    assert response.status_code == 404


def test_http_create_empty_source_ref_is_400(catalog_client: object) -> None:
    client, charges, invoices = catalog_client
    assert charges.row is not None
    assert invoices.row is not None
    response = client.post(
        "/api/v1/bookkeepings",
        headers=bearer_auth_headers(),
        json={
            "charge_id": str(charges.row.id),
            "sales_invoice_id": str(invoices.row.id),
            "source_ref": "   ",
        },
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]
