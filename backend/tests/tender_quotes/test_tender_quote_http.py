from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.tender_quote import (
    require_bid_source_ref,
    require_order_limit,
    require_quote_id,
    require_valid_until,
)
from app.main import app
from app.models.quotation import Quotation
from app.models.tender_quote import TenderQuote
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


class StubQuotationService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: Quotation | None = None

    async def get_quotation(self, quotation_id: UUID) -> Quotation:
        if self.row is None or self.row.id != quotation_id:
            raise ResourceNotFound("nieznana wycena")
        return self.row


class StubTenderQuoteService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[TenderQuote] = []

    async def list_bids(self) -> list[TenderQuote]:
        return list(self.rows)

    async def record_bid(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        quotation_id: object,
        valid_until: object,
        order_limit: object,
        source_ref: object,
    ) -> TenderQuote:
        row = TenderQuote(
            id=uuid4(),
            organization_id=organization_id,
            quotation_id=require_quote_id(quotation_id),
            valid_until=require_valid_until(valid_until),
            order_limit=require_order_limit(order_limit),
            source_ref=require_bid_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


def _offer() -> Quotation:
    return Quotation(
        id=uuid4(),
        organization_id=uuid4(),
        charge_code="THC",
        rate_line_id=uuid4(),
        amount=Decimal("10.0000"),
        currency="EUR",
        source_ref="fixture://quotation/1",
        created_by=uuid4(),
    )


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    bids = StubTenderQuoteService(object())
    quotes = StubQuotationService(object())
    quotes.row = _offer()

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.tender_quotes.TenderQuoteService", lambda _s: bids)
    monkeypatch.setattr("app.api.tender_quotes.QuotationService", lambda _s: quotes)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), bids, quotes
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(quotation_id: UUID, **overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "quotation_id": str(quotation_id),
        "valid_until": "2026-12-31",
        "order_limit": 3,
        "source_ref": "fixture://tender-quote/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_tender_quote(catalog_client: object) -> None:
    client, _bids, quotes = catalog_client
    assert quotes.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/tender-quotes",
        headers=headers,
        json=_payload(quotes.row.id),
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["order_limit"] == 3
    assert body["valid_until"] == "2026-12-31"
    assert "buy_amount" not in body
    listed = client.get("/api/v1/tender-quotes", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_bid_zero_limit_is_400(catalog_client: object) -> None:
    client, _bids, quotes = catalog_client
    assert quotes.row is not None
    response = client.post(
        "/api/v1/tender-quotes",
        headers=bearer_auth_headers(),
        json=_payload(quotes.row.id, order_limit=0),
    )
    assert response.status_code == 400
    assert "limit" in response.json()["detail"]


def test_http_create_bid_bad_date_is_400(catalog_client: object) -> None:
    client, _bids, quotes = catalog_client
    assert quotes.row is not None
    response = client.post(
        "/api/v1/tender-quotes",
        headers=bearer_auth_headers(),
        json=_payload(quotes.row.id, valid_until="31-12-2026"),
    )
    assert response.status_code == 400
    assert "data" in response.json()["detail"]


def test_http_create_bid_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _bids, quotes = catalog_client
    assert quotes.row is not None
    response = client.post(
        "/api/v1/tender-quotes",
        headers=bearer_auth_headers(),
        json=_payload(quotes.row.id, source_ref="http://hold.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
