from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.money_cost import require_cost_source_ref
from app.main import app
from app.models.money_cost import MoneyCost
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


class StubBankPaymentService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: _Row | None = None

    async def get_payment(self, payment_id: UUID) -> _Row:
        if self.row is None or self.row.id != payment_id:
            raise ResourceNotFound("nieznana płatność")
        return self.row


class StubNbpRateService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: _Row | None = None

    async def get_rate(self, rate_id: UUID) -> _Row:
        if self.row is None or self.row.id != rate_id:
            raise ResourceNotFound("nieznany kurs")
        return self.row


class StubCostService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[MoneyCost] = []

    async def list_costs(self) -> list[MoneyCost]:
        return list(self.rows)

    async def record_cost(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        bank_payment_id: UUID,
        nbp_rate_id: UUID,
        source_ref: str,
    ) -> MoneyCost:
        row = MoneyCost(
            id=uuid4(),
            organization_id=organization_id,
            bank_payment_id=bank_payment_id,
            nbp_rate_id=nbp_rate_id,
            source_ref=require_cost_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    payments = StubBankPaymentService(object())
    rates = StubNbpRateService(object())
    costs = StubCostService(object())

    def _payments(_session: object) -> StubBankPaymentService:
        return payments

    def _rates(_session: object) -> StubNbpRateService:
        return rates

    def _rows(_session: object) -> StubCostService:
        return costs

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.money_costs.BankPaymentService", _payments)
    monkeypatch.setattr("app.api.money_costs.NbpRateService", _rates)
    monkeypatch.setattr("app.api.money_costs.MoneyCostService", _rows)
    payments.row = _Row(uuid4())
    rates.row = _Row(uuid4())
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), payments, rates
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_cost(catalog_client: object) -> None:
    client, payments, rates = catalog_client
    assert payments.row is not None
    assert rates.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/money-costs",
        headers=headers,
        json={
            "bank_payment_id": str(payments.row.id),
            "nbp_rate_id": str(rates.row.id),
            "source_ref": "fixture://money-cost/1",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["bank_payment_id"] == str(payments.row.id)
    assert body["nbp_rate_id"] == str(rates.row.id)
    assert "amount" not in body
    assert "buy_amount" not in body
    assert "wacc" not in body
    assert "mid" not in body
    listed = client.get("/api/v1/money-costs", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_unknown_payment_is_404(catalog_client: object) -> None:
    client, _payments, rates = catalog_client
    assert rates.row is not None
    response = client.post(
        "/api/v1/money-costs",
        headers=bearer_auth_headers(),
        json={
            "bank_payment_id": str(uuid4()),
            "nbp_rate_id": str(rates.row.id),
            "source_ref": "fixture://money-cost/1",
        },
    )
    assert response.status_code == 404


def test_http_create_unknown_rate_is_404(catalog_client: object) -> None:
    client, payments, _rates = catalog_client
    assert payments.row is not None
    response = client.post(
        "/api/v1/money-costs",
        headers=bearer_auth_headers(),
        json={
            "bank_payment_id": str(payments.row.id),
            "nbp_rate_id": str(uuid4()),
            "source_ref": "fixture://money-cost/1",
        },
    )
    assert response.status_code == 404


def test_http_create_empty_source_ref_is_400(catalog_client: object) -> None:
    client, payments, rates = catalog_client
    assert payments.row is not None
    assert rates.row is not None
    response = client.post(
        "/api/v1/money-costs",
        headers=bearer_auth_headers(),
        json={
            "bank_payment_id": str(payments.row.id),
            "nbp_rate_id": str(rates.row.id),
            "source_ref": "   ",
        },
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]
