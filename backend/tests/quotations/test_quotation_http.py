from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import QuotationGap, UnknownChargeCode
from app.main import app
from app.models.quotation import Quotation
from tests.http_auth import bearer_auth_headers


def _lane_body(charge_code: str = "THC") -> dict[str, str]:
    return {
        "charge_code": charge_code,
        "origin_port_id": str(uuid4()),
        "destination_port_id": str(uuid4()),
        "party_id": str(uuid4()),
    }


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


class DenyAllAuthz:
    async def check(self, *, user_id, relation, object_type, object_id) -> bool:
        return False


class StubQuotationService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[Quotation] = []

    async def list_quotations(
        self,
        *,
        party_id: UUID | None = None,
        origin_port_id: UUID | None = None,
        destination_port_id: UUID | None = None,
    ) -> list[Quotation]:
        return list(self.rows)

    async def quote_from_current_rate(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        charge_code: str,
        origin_port_id: UUID | None,
        destination_port_id: UUID | None,
        party_id: UUID | None,
    ) -> Quotation:
        token = charge_code.strip().upper()
        if token == "LOOSE":
            raise UnknownChargeCode("nieznany kod opłaty: LOOSE")
        if token == "GAP":
            raise QuotationGap("quotation_gap: brak bieżącej stawki dla GAP")
        row = Quotation(
            id=uuid4(),
            organization_id=organization_id,
            charge_code=token,
            rate_line_id=uuid4(),
            amount=Decimal("10.5000"),
            currency="EUR",
            source_ref="tariff://a",
            created_by=user_id,
            origin_port_id=origin_port_id,
            destination_port_id=destination_port_id,
            party_id=party_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def quotations_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    stub = StubQuotationService(object())

    def _factory(session: object) -> StubQuotationService:
        return stub

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.quotations.QuotationService", _factory)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_quote_and_list(quotations_client: TestClient) -> None:
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = quotations_client.post(
        "/api/v1/quotations",
        headers=headers,
        json=_lane_body("THC"),
    )
    assert created.status_code == 201
    body = created.json()
    assert body["charge_code"] == "THC"
    assert body["amount"] == "10.5000"
    assert body["currency"] == "EUR"
    assert body["source_ref"] == "tariff://a"
    assert body["organization_id"] == str(org_id)
    assert isinstance(body["amount"], str)
    assert "buy_amount" not in body

    listed = quotations_client.get("/api/v1/quotations", headers=headers)
    assert listed.status_code == 200
    rows = listed.json()
    assert len(rows) == 1
    assert rows[0]["id"] == body["id"]


def test_http_rejects_unknown_charge_code(quotations_client: TestClient) -> None:
    response = quotations_client.post(
        "/api/v1/quotations",
        headers=bearer_auth_headers(),
        json=_lane_body("LOOSE"),
    )
    assert response.status_code == 400
    assert "LOOSE" in response.json()["detail"]


def test_http_quotation_gap(quotations_client: TestClient) -> None:
    response = quotations_client.post(
        "/api/v1/quotations",
        headers=bearer_auth_headers(),
        json=_lane_body("GAP"),
    )
    assert response.status_code == 400
    assert "quotation_gap" in response.json()["detail"]


def test_http_rejects_amount_in_body(quotations_client: TestClient) -> None:
    response = quotations_client.post(
        "/api/v1/quotations",
        headers=bearer_auth_headers(),
        json={**_lane_body("THC"), "amount": "99.0000"},
    )
    assert response.status_code == 422


def test_http_rejects_quote_without_lane_and_party(quotations_client: TestClient) -> None:
    response = quotations_client.post(
        "/api/v1/quotations",
        headers=bearer_auth_headers(),
        json={"charge_code": "THC"},
    )
    assert response.status_code == 422


def test_http_quote_returns_snapshot_ids(quotations_client: TestClient) -> None:
    origin = uuid4()
    destination = uuid4()
    party = uuid4()
    response = quotations_client.post(
        "/api/v1/quotations",
        headers=bearer_auth_headers(),
        json={
            "charge_code": "THC",
            "origin_port_id": str(origin),
            "destination_port_id": str(destination),
            "party_id": str(party),
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["origin_port_id"] == str(origin)
    assert body["destination_port_id"] == str(destination)
    assert body["party_id"] == str(party)


def test_list_quotations_forbidden_without_permission() -> None:
    set_authz_checker(DenyAllAuthz())
    client = TestClient(app)
    response = client.get(
        "/api/v1/quotations",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 403
    set_authz_checker(None)
