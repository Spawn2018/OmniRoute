from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import UnknownParty, UnknownPartyScorecard
from app.main import app
from app.models.party_scorecard import PartyScorecard
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


class StubPartyService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[PartyScorecard] = []

    async def list_scorecards(self) -> list[PartyScorecard]:
        return list(self.rows)

    async def get_scorecard(self, party_id: UUID) -> PartyScorecard:
        for row in self.rows:
            if row.party_id == party_id:
                return row
        raise UnknownPartyScorecard(f"brak karty wyników: {party_id}")

    async def upsert_scorecard(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        party_id: UUID,
        response_rate: object | None = None,
        median_response_hours: object | None = None,
        price_position: object | None = None,
        quote_invoice_match_rate: object | None = None,
        rollover_count: object | None = None,
        sample_size: object | None = None,
        window_days: object | None = None,
    ) -> PartyScorecard:
        if str(party_id) == "00000000-0000-0000-0000-000000000000":
            raise UnknownParty(f"nieznany kontrahent: {party_id}")
        row = PartyScorecard(
            id=uuid4(),
            organization_id=organization_id,
            party_id=party_id,
            window_days=90 if window_days is None else int(window_days),
            sample_size=0 if sample_size is None else int(sample_size),
            response_rate=None if response_rate in (None, "") else Decimal(str(response_rate)),
            median_response_hours=(
                None if median_response_hours in (None, "") else Decimal(str(median_response_hours))
            ),
            price_position=None if price_position in (None, "") else Decimal(str(price_position)),
            quote_invoice_match_rate=(
                None
                if quote_invoice_match_rate in (None, "")
                else Decimal(str(quote_invoice_match_rate))
            ),
            rollover_count=rollover_count,
            source_ref="tenant:manual",
            computed_at=datetime.now(UTC),
            created_by=user_id,
        )
        self.rows = [item for item in self.rows if item.party_id != party_id]
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    stub = StubPartyService(object())

    def _factory(session: object) -> StubPartyService:
        return stub

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.party_scorecards.PartyService", _factory)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_upsert_and_list_scorecards(catalog_client: TestClient) -> None:
    org_id = uuid4()
    party_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    saved = catalog_client.post(
        f"/api/v1/party-scorecards/{party_id}",
        headers=headers,
        json={"response_rate": "0.8000", "sample_size": 5, "window_days": 90},
    )
    assert saved.status_code == 200
    body = saved.json()
    assert body["party_id"] == str(party_id)
    assert body["organization_id"] == str(org_id)
    assert body["response_rate"] == "0.8000"
    assert body["source_ref"] == "tenant:manual"
    assert "amount" not in body
    assert "credit_limit" not in body

    listed = catalog_client.get("/api/v1/party-scorecards", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]

    fetched = catalog_client.get(f"/api/v1/party-scorecards/{party_id}", headers=headers)
    assert fetched.status_code == 200
    assert fetched.json()["id"] == body["id"]


def test_http_missing_scorecard_is_rejected(catalog_client: TestClient) -> None:
    response = catalog_client.get(
        f"/api/v1/party-scorecards/{uuid4()}",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 400
    assert "brak karty" in response.json()["detail"]


def test_http_upsert_unknown_party_is_rejected(catalog_client: TestClient) -> None:
    response = catalog_client.post(
        "/api/v1/party-scorecards/00000000-0000-0000-0000-000000000000",
        headers=bearer_auth_headers(),
        json={"sample_size": 0, "window_days": 90},
    )
    assert response.status_code == 400
    assert "nieznany kontrahent" in response.json()["detail"]


def test_http_upsert_rejects_client_source_ref(catalog_client: TestClient) -> None:
    response = catalog_client.post(
        f"/api/v1/party-scorecards/{uuid4()}",
        headers=bearer_auth_headers(),
        json={"sample_size": 0, "window_days": 90, "source_ref": "forged:origin"},
    )
    assert response.status_code == 422
