from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.quote_invoice_settlement import require_settlement_source_ref
from app.main import app
from app.models.quote_invoice_settlement import QuoteInvoiceSettlement
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


class StubQuotationService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: _Row | None = None

    async def get_quotation(self, quotation_id: UUID) -> _Row:
        if self.row is None or self.row.id != quotation_id:
            raise ResourceNotFound("nieznana wycena")
        return self.row


class StubSalesInvoiceService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: _Row | None = None

    async def get_invoice(self, invoice_id: UUID) -> _Row:
        if self.row is None or self.row.id != invoice_id:
            raise ResourceNotFound("nieznana faktura")
        return self.row


class StubSettlementService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[QuoteInvoiceSettlement] = []

    async def list_settlements(self) -> list[QuoteInvoiceSettlement]:
        return list(self.rows)

    async def record_settlement(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        quotation_id: UUID,
        sales_invoice_id: UUID,
        source_ref: str,
    ) -> QuoteInvoiceSettlement:
        row = QuoteInvoiceSettlement(
            id=uuid4(),
            organization_id=organization_id,
            quotation_id=quotation_id,
            sales_invoice_id=sales_invoice_id,
            source_ref=require_settlement_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    quotes = StubQuotationService(object())
    invoices = StubSalesInvoiceService(object())
    settlements = StubSettlementService(object())

    def _quotes(_session: object) -> StubQuotationService:
        return quotes

    def _invoices(_session: object) -> StubSalesInvoiceService:
        return invoices

    def _rows(_session: object) -> StubSettlementService:
        return settlements

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.quote_invoice_settlements.QuotationService", _quotes)
    monkeypatch.setattr("app.api.quote_invoice_settlements.SalesInvoiceService", _invoices)
    monkeypatch.setattr(
        "app.api.quote_invoice_settlements.QuoteInvoiceSettlementService",
        _rows,
    )
    quotes.row = _Row(uuid4())
    invoices.row = _Row(uuid4())
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), quotes, invoices
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_settlement(catalog_client: object) -> None:
    client, quotes, invoices = catalog_client
    assert quotes.row is not None
    assert invoices.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/quote-invoice-settlements",
        headers=headers,
        json={
            "quotation_id": str(quotes.row.id),
            "sales_invoice_id": str(invoices.row.id),
            "source_ref": "fixture://quote-invoice-settlement/1",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["quotation_id"] == str(quotes.row.id)
    assert body["sales_invoice_id"] == str(invoices.row.id)
    assert "amount" not in body
    assert "sell_amount" not in body
    assert "ksef" not in body
    listed = client.get("/api/v1/quote-invoice-settlements", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_unknown_quotation_is_404(catalog_client: object) -> None:
    client, _quotes, invoices = catalog_client
    assert invoices.row is not None
    response = client.post(
        "/api/v1/quote-invoice-settlements",
        headers=bearer_auth_headers(),
        json={
            "quotation_id": str(uuid4()),
            "sales_invoice_id": str(invoices.row.id),
            "source_ref": "fixture://quote-invoice-settlement/1",
        },
    )
    assert response.status_code == 404


def test_http_create_unknown_invoice_is_404(catalog_client: object) -> None:
    client, quotes, _invoices = catalog_client
    assert quotes.row is not None
    response = client.post(
        "/api/v1/quote-invoice-settlements",
        headers=bearer_auth_headers(),
        json={
            "quotation_id": str(quotes.row.id),
            "sales_invoice_id": str(uuid4()),
            "source_ref": "fixture://quote-invoice-settlement/1",
        },
    )
    assert response.status_code == 404


def test_http_create_empty_source_ref_is_400(catalog_client: object) -> None:
    client, quotes, invoices = catalog_client
    assert quotes.row is not None
    assert invoices.row is not None
    response = client.post(
        "/api/v1/quote-invoice-settlements",
        headers=bearer_auth_headers(),
        json={
            "quotation_id": str(quotes.row.id),
            "sales_invoice_id": str(invoices.row.id),
            "source_ref": "   ",
        },
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]
