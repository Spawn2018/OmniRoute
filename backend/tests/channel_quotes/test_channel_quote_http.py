from datetime import date
from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import UnknownCarrierProfile, UnknownChannelQuote
from app.main import app
from app.models.channel_quote import ChannelQuote
from tests.http_auth import bearer_auth_headers

_MISSING_CARRIER = UUID("00000000-0000-0000-0000-000000000000")


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


class StubChannelQuoteService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[ChannelQuote] = []

    async def list_quotes(self) -> list[ChannelQuote]:
        return list(self.rows)

    async def resolve(
        self,
        *,
        party_id: UUID,
        origin_port_id: UUID,
        destination_port_id: UUID,
        on_date: date,
    ) -> ChannelQuote:
        matches = [
            row
            for row in self.rows
            if row.party_id == party_id
            and row.origin_port_id == origin_port_id
            and row.destination_port_id == destination_port_id
            and row.quote_date <= on_date
        ]
        if not matches:
            raise UnknownChannelQuote(f"brak oferty kanału na {on_date.isoformat()}")
        return max(matches, key=lambda row: row.quote_date)

    async def create_quote(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        party_id: UUID,
        origin_port_id: UUID,
        destination_port_id: UUID,
        quote_date: date,
        amount: object,
        currency: object,
    ) -> ChannelQuote:
        if party_id == _MISSING_CARRIER:
            raise UnknownCarrierProfile(f"brak profilu armatora: {party_id}")
        row = ChannelQuote(
            id=uuid4(),
            organization_id=organization_id,
            amount=Decimal(str(amount)),
            currency=str(currency).strip().upper(),
            party_id=party_id,
            origin_port_id=origin_port_id,
            destination_port_id=destination_port_id,
            quote_date=quote_date,
            source_ref="tenant:manual",
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    stub = StubChannelQuoteService(object())

    def _factory(session: object) -> StubChannelQuoteService:
        return stub

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.channel_quotes.ChannelQuoteService", _factory)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_list_and_resolve(catalog_client: TestClient) -> None:
    org_id = uuid4()
    party_id = uuid4()
    origin_id = uuid4()
    dest_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = catalog_client.post(
        "/api/v1/channel-quotes",
        headers=headers,
        json={
            "party_id": str(party_id),
            "origin_port_id": str(origin_id),
            "destination_port_id": str(dest_id),
            "quote_date": "2026-09-01",
            "amount": "1200.0000",
            "currency": "USD",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["party_id"] == str(party_id)
    assert body["organization_id"] == str(org_id)
    assert body["amount"] == "1200.0000"
    assert isinstance(body["amount"], str)
    assert body["currency"] == "USD"
    assert body["source_ref"] == "tenant:manual"
    assert "buy_amount" not in body
    assert "margin" not in body

    listed = catalog_client.get("/api/v1/channel-quotes", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]

    resolved = catalog_client.get(
        "/api/v1/channel-quotes/resolve",
        headers=headers,
        params={
            "party_id": str(party_id),
            "origin_port_id": str(origin_id),
            "destination_port_id": str(dest_id),
            "on_date": "2026-09-05",
        },
    )
    assert resolved.status_code == 200
    assert resolved.json()["id"] == body["id"]


def test_http_resolve_unknown_is_rejected(catalog_client: TestClient) -> None:
    response = catalog_client.get(
        "/api/v1/channel-quotes/resolve",
        headers=bearer_auth_headers(),
        params={
            "party_id": str(uuid4()),
            "origin_port_id": str(uuid4()),
            "destination_port_id": str(uuid4()),
            "on_date": "2026-09-01",
        },
    )
    assert response.status_code == 400
    assert "brak oferty kanału" in response.json()["detail"]


def test_http_create_unknown_carrier_is_rejected(catalog_client: TestClient) -> None:
    response = catalog_client.post(
        "/api/v1/channel-quotes",
        headers=bearer_auth_headers(),
        json={
            "party_id": str(_MISSING_CARRIER),
            "origin_port_id": str(uuid4()),
            "destination_port_id": str(uuid4()),
            "quote_date": "2026-09-01",
            "amount": "10.0000",
            "currency": "USD",
        },
    )
    assert response.status_code == 400
    assert "profilu armatora" in response.json()["detail"]


def test_http_create_rejects_client_source_ref(catalog_client: TestClient) -> None:
    response = catalog_client.post(
        "/api/v1/channel-quotes",
        headers=bearer_auth_headers(),
        json={
            "party_id": str(uuid4()),
            "origin_port_id": str(uuid4()),
            "destination_port_id": str(uuid4()),
            "quote_date": "2026-09-01",
            "amount": "10.0000",
            "currency": "USD",
            "source_ref": "forged:origin",
        },
    )
    assert response.status_code == 422
