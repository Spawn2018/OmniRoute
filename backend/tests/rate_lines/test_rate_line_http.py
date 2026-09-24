from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import InvalidSourceRef, RateLineAlreadySuperseded, ResourceNotFound
from app.domain.rate_line import require_allotment_teu, require_spot_or_contract
from app.main import app
from app.models.rate_line import RateLine
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


class StubRateLineService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[RateLine] = []

    async def list_rates(self) -> list[RateLine]:
        return list(self.rows)

    async def create_buy_rate(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        charge_code: str,
        amount: object,
        currency: object,
        source_ref: str,
        allotment_teu: object = None,
        spot_or_contract: object = None,
    ) -> RateLine:
        origin = source_ref.strip()
        if origin == "":
            raise InvalidSourceRef("source_ref jest obowiązkowy")
        if isinstance(amount, float):
            raise InvalidSourceRef("kwota nie może być float")
        teu = require_allotment_teu(allotment_teu)
        deal = require_spot_or_contract(spot_or_contract)
        row = RateLine(
            id=uuid4(),
            organization_id=organization_id,
            charge_code=charge_code.strip().upper(),
            amount=Decimal(str(amount)),
            currency=str(currency),
            allotment_teu=teu,
            spot_or_contract=deal,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row

    async def supersede(
        self,
        *,
        rate_line_id: UUID,
        user_id: UUID,
        amount: object,
        currency: object,
        source_ref: str,
        allotment_teu: object = None,
        spot_or_contract: object = None,
    ) -> RateLine:
        current = next((row for row in self.rows if row.id == rate_line_id), None)
        if current is None:
            raise ResourceNotFound("rate_line nie istnieje")
        if current.superseded_by is not None:
            raise RateLineAlreadySuperseded("rate_line już zastąpiony")
        successor = await self.create_buy_rate(
            organization_id=current.organization_id,
            user_id=user_id,
            charge_code=current.charge_code,
            amount=amount,
            currency=currency,
            source_ref=source_ref,
            allotment_teu=allotment_teu,
            spot_or_contract=spot_or_contract,
        )
        current.superseded_by = successor.id
        return successor


@pytest.fixture
def rates_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    stub = StubRateLineService(object())

    def _factory(session: object) -> StubRateLineService:
        return stub

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.rate_lines.RateLineService", _factory)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_rate_lines(rates_client: TestClient) -> None:
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = rates_client.post(
        "/api/v1/rate-lines",
        headers=headers,
        json={
            "charge_code": "THC",
            "amount": "10.5",
            "currency": "EUR",
            "source_ref": "tariff://msc-2026",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["charge_code"] == "THC"
    assert body["amount"] == "10.5000"
    assert body["currency"] == "EUR"
    assert body["source_ref"] == "tariff://msc-2026"
    assert body["allotment_teu"] is None
    assert body["spot_or_contract"] is None
    assert body["superseded_by"] is None
    assert body["organization_id"] == str(org_id)
    assert "buy" not in body
    assert "sell" not in body
    assert "margin" not in body

    listed = rates_client.get("/api/v1/rate-lines", headers=headers)
    assert listed.status_code == 200
    rows = listed.json()
    assert len(rows) == 1
    assert rows[0]["id"] == body["id"]
    assert rows[0]["amount"] == "10.5000"


def test_http_create_with_allotment_teu(rates_client: TestClient) -> None:
    created = rates_client.post(
        "/api/v1/rate-lines",
        headers=bearer_auth_headers(),
        json={
            "charge_code": "THC",
            "amount": "10",
            "currency": "EUR",
            "source_ref": "tariff://teu",
            "allotment_teu": "12.5",
        },
    )
    assert created.status_code == 201
    assert created.json()["allotment_teu"] == "12.5000"


def test_http_rejects_negative_allotment_teu(rates_client: TestClient) -> None:
    response = rates_client.post(
        "/api/v1/rate-lines",
        headers=bearer_auth_headers(),
        json={
            "charge_code": "THC",
            "amount": "10",
            "currency": "EUR",
            "source_ref": "tariff://teu",
            "allotment_teu": "-1",
        },
    )
    assert response.status_code == 400
    assert "allotment" in response.json()["detail"]


def test_http_create_with_spot_or_contract(rates_client: TestClient) -> None:
    created = rates_client.post(
        "/api/v1/rate-lines",
        headers=bearer_auth_headers(),
        json={
            "charge_code": "THC",
            "amount": "10",
            "currency": "EUR",
            "source_ref": "tariff://spot",
            "spot_or_contract": " Spot ",
        },
    )
    assert created.status_code == 201
    assert created.json()["spot_or_contract"] == "spot"


def test_http_rejects_bad_spot_or_contract(rates_client: TestClient) -> None:
    response = rates_client.post(
        "/api/v1/rate-lines",
        headers=bearer_auth_headers(),
        json={
            "charge_code": "THC",
            "amount": "10",
            "currency": "EUR",
            "source_ref": "tariff://spot",
            "spot_or_contract": "futures",
        },
    )
    assert response.status_code == 400
    assert "spot_or_contract" in response.json()["detail"]


def test_http_rejects_blank_source_ref(rates_client: TestClient) -> None:
    response = rates_client.post(
        "/api/v1/rate-lines",
        headers=bearer_auth_headers(),
        json={
            "charge_code": "THC",
            "amount": "10",
            "currency": "EUR",
            "source_ref": "   ",
        },
    )
    assert response.status_code == 400
    assert "source_ref" in response.json()["detail"]


def test_http_rejects_numeric_amount(rates_client: TestClient) -> None:
    response = rates_client.post(
        "/api/v1/rate-lines",
        headers=bearer_auth_headers(),
        json={
            "charge_code": "THC",
            "amount": 10.5,
            "currency": "EUR",
            "source_ref": "tariff://a",
        },
    )
    assert response.status_code == 422


def test_http_supersede_points_predecessor(rates_client: TestClient) -> None:
    headers = bearer_auth_headers()
    created = rates_client.post(
        "/api/v1/rate-lines",
        headers=headers,
        json={
            "charge_code": "THC",
            "amount": "10",
            "currency": "EUR",
            "source_ref": "tariff://a",
        },
    )
    rate_id = created.json()["id"]
    successor = rates_client.post(
        f"/api/v1/rate-lines/{rate_id}/supersede",
        headers=headers,
        json={"amount": "11", "currency": "EUR", "source_ref": "tariff://b"},
    )
    assert successor.status_code == 201
    listed = rates_client.get("/api/v1/rate-lines", headers=headers)
    rows = listed.json()
    predecessor = next(row for row in rows if row["id"] == rate_id)
    assert predecessor["superseded_by"] == successor.json()["id"]
    assert successor.json()["amount"] == "11.0000"


def test_http_supersede_unknown_is_not_found(rates_client: TestClient) -> None:
    response = rates_client.post(
        f"/api/v1/rate-lines/{uuid4()}/supersede",
        headers=bearer_auth_headers(),
        json={"amount": "11", "currency": "EUR", "source_ref": "tariff://b"},
    )
    assert response.status_code == 404
