from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.bank_payment import require_payment_source_ref
from app.domain.errors import ResourceNotFound
from app.main import app
from app.models.bank_payment import BankPayment
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


class StubSalesInvoiceService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: _Row | None = None

    async def get_invoice(self, invoice_id: UUID) -> _Row:
        if self.row is None or self.row.id != invoice_id:
            raise ResourceNotFound("nieznana faktura")
        return self.row


class StubPartyService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: _Row | None = None

    async def get_bank_account(self, account_id: UUID) -> _Row:
        if self.row is None or self.row.id != account_id:
            raise ResourceNotFound("nieznany rachunek")
        return self.row


class StubPaymentService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[BankPayment] = []

    async def list_payments(self) -> list[BankPayment]:
        return list(self.rows)

    async def record_payment(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        sales_invoice_id: UUID,
        party_bank_account_id: UUID,
        source_ref: str,
    ) -> BankPayment:
        row = BankPayment(
            id=uuid4(),
            organization_id=organization_id,
            sales_invoice_id=sales_invoice_id,
            party_bank_account_id=party_bank_account_id,
            source_ref=require_payment_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    invoices = StubSalesInvoiceService(object())
    accounts = StubPartyService(object())
    payments = StubPaymentService(object())

    def _invoices(_session: object) -> StubSalesInvoiceService:
        return invoices

    def _accounts(_session: object) -> StubPartyService:
        return accounts

    def _rows(_session: object) -> StubPaymentService:
        return payments

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.bank_payments.SalesInvoiceService", _invoices)
    monkeypatch.setattr("app.api.bank_payments.PartyService", _accounts)
    monkeypatch.setattr("app.api.bank_payments.BankPaymentService", _rows)
    invoices.row = _Row(uuid4())
    accounts.row = _Row(uuid4())
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), invoices, accounts
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_payment(catalog_client: object) -> None:
    client, invoices, accounts = catalog_client
    assert invoices.row is not None
    assert accounts.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/bank-payments",
        headers=headers,
        json={
            "sales_invoice_id": str(invoices.row.id),
            "party_bank_account_id": str(accounts.row.id),
            "source_ref": "fixture://bank-payment/1",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["sales_invoice_id"] == str(invoices.row.id)
    assert body["party_bank_account_id"] == str(accounts.row.id)
    assert "amount" not in body
    assert "sell_amount" not in body
    assert "sepa" not in body
    listed = client.get("/api/v1/bank-payments", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_unknown_invoice_is_404(catalog_client: object) -> None:
    client, _invoices, accounts = catalog_client
    assert accounts.row is not None
    response = client.post(
        "/api/v1/bank-payments",
        headers=bearer_auth_headers(),
        json={
            "sales_invoice_id": str(uuid4()),
            "party_bank_account_id": str(accounts.row.id),
            "source_ref": "fixture://bank-payment/1",
        },
    )
    assert response.status_code == 404


def test_http_create_unknown_account_is_404(catalog_client: object) -> None:
    client, invoices, _accounts = catalog_client
    assert invoices.row is not None
    response = client.post(
        "/api/v1/bank-payments",
        headers=bearer_auth_headers(),
        json={
            "sales_invoice_id": str(invoices.row.id),
            "party_bank_account_id": str(uuid4()),
            "source_ref": "fixture://bank-payment/1",
        },
    )
    assert response.status_code == 404


def test_http_create_empty_source_ref_is_400(catalog_client: object) -> None:
    client, invoices, accounts = catalog_client
    assert invoices.row is not None
    assert accounts.row is not None
    response = client.post(
        "/api/v1/bank-payments",
        headers=bearer_auth_headers(),
        json={
            "sales_invoice_id": str(invoices.row.id),
            "party_bank_account_id": str(accounts.row.id),
            "source_ref": "   ",
        },
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]
