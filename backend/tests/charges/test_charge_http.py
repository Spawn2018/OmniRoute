from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.charge import margin
from app.domain.errors import InvalidSourceRef, MixedCurrencyCharge, UnknownChargeCode
from app.domain.money import Money
from app.main import app
from app.models.charge import Charge
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


class StubChargeService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[Charge] = []

    async def list_charges(self) -> list[tuple[Charge, Decimal]]:
        return [(row, row.sell_amount - row.buy_amount) for row in self.rows]

    async def create_charge(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        charge_code: str,
        buy_amount: object,
        buy_currency: object,
        sell_amount: object,
        sell_currency: object,
        rate_line_id: UUID | None,
        source_ref: object,
    ) -> Charge:
        if isinstance(buy_amount, float) or isinstance(sell_amount, float):
            raise MixedCurrencyCharge("kwota nie może być float")
        if type(source_ref) is not str or source_ref.strip() == "":
            raise InvalidSourceRef("source_ref jest obowiązkowy")
        buy = Money.of(buy_amount, buy_currency)
        sell = Money.of(sell_amount, sell_currency)
        margin(buy, sell)
        if charge_code.strip().upper() == "LOOSE":
            raise UnknownChargeCode("nieznany kod opłaty: LOOSE")
        row = Charge(
            id=uuid4(),
            organization_id=organization_id,
            charge_code=charge_code.strip().upper(),
            buy_amount=buy.amount,
            buy_currency=buy.currency.code,
            sell_amount=sell.amount,
            sell_currency=sell.currency.code,
            rate_line_id=rate_line_id,
            source_ref=source_ref.strip(),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def charges_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    stub = StubChargeService(object())

    def _factory(session: object) -> StubChargeService:
        return stub

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.charges.ChargeService", _factory)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_charges(charges_client: TestClient) -> None:
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = charges_client.post(
        "/api/v1/charges",
        headers=headers,
        json={
            "charge_code": "THC",
            "buy_amount": "10.5",
            "buy_currency": "EUR",
            "sell_amount": "14",
            "sell_currency": "EUR",
            "source_ref": "tenant:manual",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["charge_code"] == "THC"
    assert body["buy_amount"] == "10.5000"
    assert body["sell_amount"] == "14.0000"
    assert body["margin_amount"] == "3.5000"
    assert body["margin_currency"] == "EUR"
    assert body["buy_currency"] == "EUR"
    assert body["organization_id"] == str(org_id)
    assert body["rate_line_id"] is None
    assert body["source_ref"] == "tenant:manual"
    assert isinstance(body["margin_amount"], str)

    listed = charges_client.get("/api/v1/charges", headers=headers)
    assert listed.status_code == 200
    rows = listed.json()
    assert len(rows) == 1
    assert rows[0]["id"] == body["id"]
    assert rows[0]["margin_amount"] == "3.5000"


def test_http_rejects_mixed_currency(charges_client: TestClient) -> None:
    response = charges_client.post(
        "/api/v1/charges",
        headers=bearer_auth_headers(),
        json={
            "charge_code": "THC",
            "buy_amount": "10",
            "buy_currency": "EUR",
            "sell_amount": "14",
            "sell_currency": "USD",
            "source_ref": "tenant:manual",
        },
    )
    assert response.status_code == 400
    assert "walutę" in response.json()["detail"]


def test_http_rejects_numeric_buy_amount(charges_client: TestClient) -> None:
    response = charges_client.post(
        "/api/v1/charges",
        headers=bearer_auth_headers(),
        json={
            "charge_code": "THC",
            "buy_amount": 10.5,
            "buy_currency": "EUR",
            "sell_amount": "14",
            "sell_currency": "EUR",
            "source_ref": "tenant:manual",
        },
    )
    assert response.status_code == 422


def test_http_rejects_unknown_charge_code(charges_client: TestClient) -> None:
    response = charges_client.post(
        "/api/v1/charges",
        headers=bearer_auth_headers(),
        json={
            "charge_code": "LOOSE",
            "buy_amount": "10",
            "buy_currency": "EUR",
            "sell_amount": "14",
            "sell_currency": "EUR",
            "source_ref": "tenant:manual",
        },
    )
    assert response.status_code == 400
    assert "LOOSE" in response.json()["detail"]


def test_http_rejects_blank_source_ref(charges_client: TestClient) -> None:
    response = charges_client.post(
        "/api/v1/charges",
        headers=bearer_auth_headers(),
        json={
            "charge_code": "THC",
            "buy_amount": "10",
            "buy_currency": "EUR",
            "sell_amount": "14",
            "sell_currency": "EUR",
            "source_ref": "   ",
        },
    )
    assert response.status_code == 400
    assert "source_ref" in response.json()["detail"]
