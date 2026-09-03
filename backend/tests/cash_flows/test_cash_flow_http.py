from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.cash_flow import require_cash_flow_source_ref
from app.domain.errors import ResourceNotFound
from app.main import app
from app.models.cash_flow import CashFlow
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


class StubBankPaymentService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: _Row | None = None

    async def get_payment(self, payment_id: UUID) -> _Row:
        if self.row is None or self.row.id != payment_id:
            raise ResourceNotFound("nieznana płatność")
        return self.row


class StubCashFlowService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[CashFlow] = []

    async def list_flows(self) -> list[CashFlow]:
        return list(self.rows)

    async def record_flow(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        quotation_id: UUID,
        bank_payment_id: UUID,
        source_ref: str,
    ) -> CashFlow:
        row = CashFlow(
            id=uuid4(),
            organization_id=organization_id,
            quotation_id=quotation_id,
            bank_payment_id=bank_payment_id,
            source_ref=require_cash_flow_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    quotes = StubQuotationService(object())
    payments = StubBankPaymentService(object())
    flows = StubCashFlowService(object())

    def _quotes(_session: object) -> StubQuotationService:
        return quotes

    def _payments(_session: object) -> StubBankPaymentService:
        return payments

    def _rows(_session: object) -> StubCashFlowService:
        return flows

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.cash_flows.QuotationService", _quotes)
    monkeypatch.setattr("app.api.cash_flows.BankPaymentService", _payments)
    monkeypatch.setattr("app.api.cash_flows.CashFlowService", _rows)
    quotes.row = _Row(uuid4())
    payments.row = _Row(uuid4())
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), quotes, payments
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_cash_flow(catalog_client: object) -> None:
    client, quotes, payments = catalog_client
    assert quotes.row is not None
    assert payments.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/cash-flows",
        headers=headers,
        json={
            "quotation_id": str(quotes.row.id),
            "bank_payment_id": str(payments.row.id),
            "source_ref": "fixture://cash-flow/1",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["quotation_id"] == str(quotes.row.id)
    assert body["bank_payment_id"] == str(payments.row.id)
    assert "amount" not in body
    assert "buy_amount" not in body
    assert "sell_amount" not in body
    assert "outflow" not in body
    listed = client.get("/api/v1/cash-flows", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_unknown_quotation_is_404(catalog_client: object) -> None:
    client, _quotes, payments = catalog_client
    assert payments.row is not None
    response = client.post(
        "/api/v1/cash-flows",
        headers=bearer_auth_headers(),
        json={
            "quotation_id": str(uuid4()),
            "bank_payment_id": str(payments.row.id),
            "source_ref": "fixture://cash-flow/1",
        },
    )
    assert response.status_code == 404


def test_http_create_unknown_payment_is_404(catalog_client: object) -> None:
    client, quotes, _payments = catalog_client
    assert quotes.row is not None
    response = client.post(
        "/api/v1/cash-flows",
        headers=bearer_auth_headers(),
        json={
            "quotation_id": str(quotes.row.id),
            "bank_payment_id": str(uuid4()),
            "source_ref": "fixture://cash-flow/1",
        },
    )
    assert response.status_code == 404


def test_http_create_empty_source_ref_is_400(catalog_client: object) -> None:
    client, quotes, payments = catalog_client
    assert quotes.row is not None
    assert payments.row is not None
    response = client.post(
        "/api/v1/cash-flows",
        headers=bearer_auth_headers(),
        json={
            "quotation_id": str(quotes.row.id),
            "bank_payment_id": str(payments.row.id),
            "source_ref": "   ",
        },
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]
