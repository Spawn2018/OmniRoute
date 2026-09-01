from datetime import date
from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import UnknownNbpRate
from app.main import app
from app.models.nbp_rate import NbpRate
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


class StubNbpRateService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[NbpRate] = []

    async def list_rates(self) -> list[NbpRate]:
        return list(self.rows)

    async def create_rate(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        currency: str,
        rate_date: date,
        mid: object,
    ) -> NbpRate:
        row = NbpRate(
            id=uuid4(),
            organization_id=organization_id,
            currency=currency.strip().upper(),
            rate_date=rate_date,
            mid=Decimal(str(mid)),
            source_ref="tenant:manual",
            created_by=user_id,
        )
        self.rows.append(row)
        return row

    async def resolve(self, currency: str, on_date: date) -> NbpRate:
        token = currency.strip().upper()
        matches = [row for row in self.rows if row.currency == token and row.rate_date <= on_date]
        if not matches:
            raise UnknownNbpRate(f"brak kursu NBP {token} na {on_date.isoformat()}")
        return max(matches, key=lambda row: row.rate_date)


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    stub = StubNbpRateService(object())

    def _factory(session: object) -> StubNbpRateService:
        return stub

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.nbp_rates.NbpRateService", _factory)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_nbp_rates(catalog_client: TestClient) -> None:
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = catalog_client.post(
        "/api/v1/nbp-rates",
        headers=headers,
        json={"currency": "EUR", "rate_date": "2026-09-01", "mid": "4.2500"},
    )
    assert created.status_code == 201
    body = created.json()
    assert body["currency"] == "EUR"
    assert body["organization_id"] == str(org_id)
    assert body["rate_date"] == "2026-09-01"
    assert body["mid"] == "4.2500"
    assert isinstance(body["mid"], str)
    assert body["source_ref"] == "tenant:manual"
    assert "amount" not in body

    listed = catalog_client.get("/api/v1/nbp-rates", headers=headers)
    assert listed.status_code == 200
    rows = listed.json()
    assert len(rows) == 1
    assert rows[0]["id"] == body["id"]
    assert isinstance(rows[0]["mid"], str)


def test_http_resolve_unknown_currency_is_rejected(catalog_client: TestClient) -> None:
    response = catalog_client.get(
        "/api/v1/nbp-rates/resolve",
        headers=bearer_auth_headers(),
        params={"currency": "EUR", "on_date": "2026-09-01"},
    )
    assert response.status_code == 400
    assert "brak kursu NBP EUR" in response.json()["detail"]


def test_http_create_rejects_client_source_ref(catalog_client: TestClient) -> None:
    response = catalog_client.post(
        "/api/v1/nbp-rates",
        headers=bearer_auth_headers(),
        json={
            "currency": "EUR",
            "rate_date": "2026-09-01",
            "mid": "4.2500",
            "source_ref": "forged:origin",
        },
    )
    assert response.status_code == 422


def test_http_resolve_returns_catalog_row(catalog_client: TestClient) -> None:
    headers = bearer_auth_headers()
    catalog_client.post(
        "/api/v1/nbp-rates",
        headers=headers,
        json={"currency": "EUR", "rate_date": "2026-09-01", "mid": "4.2500"},
    )
    resolved = catalog_client.get(
        "/api/v1/nbp-rates/resolve",
        headers=headers,
        params={"currency": "EUR", "on_date": "2026-09-05"},
    )
    assert resolved.status_code == 200
    body = resolved.json()
    assert body["currency"] == "EUR"
    assert body["mid"] == "4.2500"
    assert isinstance(body["mid"], str)
