from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.cost_to_serve import require_cost_to_serve_source_ref
from app.domain.errors import ResourceNotFound
from app.main import app
from app.models.cost_to_serve import CostToServe
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


class StubPartyService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: _Row | None = None

    async def get_sop(self, sop_id: UUID) -> _Row:
        if self.row is None or self.row.id != sop_id:
            raise ResourceNotFound("nieznana procedura")
        return self.row


class StubQuotationService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: _Row | None = None

    async def get_quotation(self, quotation_id: UUID) -> _Row:
        if self.row is None or self.row.id != quotation_id:
            raise ResourceNotFound("nieznana wycena")
        return self.row


class StubCostToServeService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[CostToServe] = []

    async def list_rows(self) -> list[CostToServe]:
        return list(self.rows)

    async def record_row(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        customer_sop_id: UUID,
        quotation_id: UUID,
        source_ref: str,
    ) -> CostToServe:
        row = CostToServe(
            id=uuid4(),
            organization_id=organization_id,
            customer_sop_id=customer_sop_id,
            quotation_id=quotation_id,
            source_ref=require_cost_to_serve_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    parties = StubPartyService(object())
    quotes = StubQuotationService(object())
    rows = StubCostToServeService(object())

    def _parties(_session: object) -> StubPartyService:
        return parties

    def _quotes(_session: object) -> StubQuotationService:
        return quotes

    def _rows(_session: object) -> StubCostToServeService:
        return rows

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.cost_to_serve.PartyService", _parties)
    monkeypatch.setattr("app.api.cost_to_serve.QuotationService", _quotes)
    monkeypatch.setattr("app.api.cost_to_serve.CostToServeService", _rows)
    parties.row = _Row(uuid4())
    quotes.row = _Row(uuid4())
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), parties, quotes
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_cost_to_serve(catalog_client: object) -> None:
    client, parties, quotes = catalog_client
    assert parties.row is not None
    assert quotes.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/cost-to-serves",
        headers=headers,
        json={
            "customer_sop_id": str(parties.row.id),
            "quotation_id": str(quotes.row.id),
            "source_ref": "fixture://cost-to-serve/1",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["customer_sop_id"] == str(parties.row.id)
    assert body["quotation_id"] == str(quotes.row.id)
    assert "amount" not in body
    assert "buy_amount" not in body
    assert "hourly_rate" not in body
    listed = client.get("/api/v1/cost-to-serves", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_unknown_sop_is_404(catalog_client: object) -> None:
    client, _parties, quotes = catalog_client
    assert quotes.row is not None
    response = client.post(
        "/api/v1/cost-to-serves",
        headers=bearer_auth_headers(),
        json={
            "customer_sop_id": str(uuid4()),
            "quotation_id": str(quotes.row.id),
            "source_ref": "fixture://cost-to-serve/1",
        },
    )
    assert response.status_code == 404


def test_http_create_unknown_quotation_is_404(catalog_client: object) -> None:
    client, parties, _quotes = catalog_client
    assert parties.row is not None
    response = client.post(
        "/api/v1/cost-to-serves",
        headers=bearer_auth_headers(),
        json={
            "customer_sop_id": str(parties.row.id),
            "quotation_id": str(uuid4()),
            "source_ref": "fixture://cost-to-serve/1",
        },
    )
    assert response.status_code == 404


def test_http_create_empty_source_ref_is_400(catalog_client: object) -> None:
    client, parties, quotes = catalog_client
    assert parties.row is not None
    assert quotes.row is not None
    response = client.post(
        "/api/v1/cost-to-serves",
        headers=bearer_auth_headers(),
        json={
            "customer_sop_id": str(parties.row.id),
            "quotation_id": str(quotes.row.id),
            "source_ref": "   ",
        },
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]
