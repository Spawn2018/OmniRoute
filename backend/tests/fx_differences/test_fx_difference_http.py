from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.fx_difference import require_fx_source_ref
from app.main import app
from app.models.fx_difference import FxDifference
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


class StubNbpRateService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: _Row | None = None

    async def get_rate(self, rate_id: UUID) -> _Row:
        if self.row is None or self.row.id != rate_id:
            raise ResourceNotFound("nieznany kurs")
        return self.row


class StubFxService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[FxDifference] = []

    async def list_differences(self) -> list[FxDifference]:
        return list(self.rows)

    async def record_difference(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        quotation_id: UUID,
        nbp_rate_id: UUID,
        source_ref: str,
    ) -> FxDifference:
        row = FxDifference(
            id=uuid4(),
            organization_id=organization_id,
            quotation_id=quotation_id,
            nbp_rate_id=nbp_rate_id,
            source_ref=require_fx_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    quotes = StubQuotationService(object())
    rates = StubNbpRateService(object())
    diffs = StubFxService(object())

    def _quotes(_session: object) -> StubQuotationService:
        return quotes

    def _rates(_session: object) -> StubNbpRateService:
        return rates

    def _rows(_session: object) -> StubFxService:
        return diffs

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.fx_differences.QuotationService", _quotes)
    monkeypatch.setattr("app.api.fx_differences.NbpRateService", _rates)
    monkeypatch.setattr("app.api.fx_differences.FxDifferenceService", _rows)
    quotes.row = _Row(uuid4())
    rates.row = _Row(uuid4())
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), quotes, rates
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_fx(catalog_client: object) -> None:
    client, quotes, rates = catalog_client
    assert quotes.row is not None
    assert rates.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/fx-differences",
        headers=headers,
        json={
            "quotation_id": str(quotes.row.id),
            "nbp_rate_id": str(rates.row.id),
            "source_ref": "fixture://fx-difference/1",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["quotation_id"] == str(quotes.row.id)
    assert body["nbp_rate_id"] == str(rates.row.id)
    assert "amount" not in body
    assert "buy_amount" not in body
    assert "fx_gain" not in body
    listed = client.get("/api/v1/fx-differences", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_unknown_quotation_is_404(catalog_client: object) -> None:
    client, _quotes, rates = catalog_client
    assert rates.row is not None
    response = client.post(
        "/api/v1/fx-differences",
        headers=bearer_auth_headers(),
        json={
            "quotation_id": str(uuid4()),
            "nbp_rate_id": str(rates.row.id),
            "source_ref": "fixture://fx-difference/1",
        },
    )
    assert response.status_code == 404


def test_http_create_unknown_rate_is_404(catalog_client: object) -> None:
    client, quotes, _rates = catalog_client
    assert quotes.row is not None
    response = client.post(
        "/api/v1/fx-differences",
        headers=bearer_auth_headers(),
        json={
            "quotation_id": str(quotes.row.id),
            "nbp_rate_id": str(uuid4()),
            "source_ref": "fixture://fx-difference/1",
        },
    )
    assert response.status_code == 404


def test_http_create_empty_source_ref_is_400(catalog_client: object) -> None:
    client, quotes, rates = catalog_client
    assert quotes.row is not None
    assert rates.row is not None
    response = client.post(
        "/api/v1/fx-differences",
        headers=bearer_auth_headers(),
        json={
            "quotation_id": str(quotes.row.id),
            "nbp_rate_id": str(rates.row.id),
            "source_ref": "   ",
        },
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]
