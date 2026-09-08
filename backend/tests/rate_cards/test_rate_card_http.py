from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.rate_card import (
    require_applies_when,
    require_card_amount,
    require_card_code,
    require_card_currency,
    require_card_source_ref,
)
from app.main import app
from app.models.rate_card import RateCard
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


class StubRateCardService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[RateCard] = []

    async def list_cards(self) -> list[RateCard]:
        return list(self.rows)

    async def record_card(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        card_code: str,
        applies_when: str,
        amount: str,
        currency: str,
        source_ref: str,
    ) -> RateCard:
        row = RateCard(
            id=uuid4(),
            organization_id=organization_id,
            card_code=require_card_code(card_code),
            applies_when=require_applies_when(applies_when),
            amount=require_card_amount(amount),
            currency=require_card_currency(currency),
            source_ref=require_card_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    rows = StubRateCardService(object())

    def _rows(_session: object) -> StubRateCardService:
        return rows

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.rate_cards.RateCardService", _rows)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), rows
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "card_code": "weekend",
        "applies_when": "sobota",
        "amount": "10.5000",
        "currency": "EUR",
        "source_ref": "fixture://rate-card/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_rate_card(catalog_client: object) -> None:
    client, _rows = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post("/api/v1/rate-cards", headers=headers, json=_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["card_code"] == "weekend"
    assert Decimal(body["amount"]) == Decimal("10.5000")
    assert "buy_amount" not in body
    listed = client.get("/api/v1/rate-cards", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_card_bad_code_is_400(catalog_client: object) -> None:
    client, _rows = catalog_client
    response = client.post(
        "/api/v1/rate-cards",
        headers=bearer_auth_headers(),
        json=_payload(card_code="X"),
    )
    assert response.status_code == 400
    assert "kod" in response.json()["detail"]


def test_http_create_card_empty_when_is_400(catalog_client: object) -> None:
    client, _rows = catalog_client
    response = client.post(
        "/api/v1/rate-cards",
        headers=bearer_auth_headers(),
        json=_payload(applies_when="  "),
    )
    assert response.status_code == 400
    assert "warunek" in response.json()["detail"]


def test_http_create_card_zero_amount_is_400(catalog_client: object) -> None:
    client, _rows = catalog_client
    response = client.post(
        "/api/v1/rate-cards",
        headers=bearer_auth_headers(),
        json=_payload(amount="0"),
    )
    assert response.status_code == 400
    assert "kwota" in response.json()["detail"]


def test_http_create_card_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _rows = catalog_client
    response = client.post(
        "/api/v1/rate-cards",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://hold.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
