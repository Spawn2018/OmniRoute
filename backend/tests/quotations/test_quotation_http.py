from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import (
    QuotationGap,
    ResourceNotFound,
    UnknownChannelQuote,
    UnknownChargeCode,
    UnknownCreditReview,
)
from app.domain.quotation import require_quotation_incoterm
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
        customer_rfq_id: UUID | None = None,
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
        customer_rfq_id: UUID | None = None,
        commodity_code_id: UUID | None = None,
        dangerous_good_id: UUID | None = None,
        incoterm: object = None,
        incoterms_version: object = None,
        trade_side: object = None,
        named_place: object = None,
    ) -> Quotation:
        token = charge_code.strip().upper()
        if token == "LOOSE":
            raise UnknownChargeCode("nieznany kod opłaty: LOOSE")
        if token == "GAP":
            raise QuotationGap("quotation_gap: brak bieżącej stawki dla GAP")
        rule, version, side, place = require_quotation_incoterm(
            incoterm, incoterms_version, trade_side, named_place,
        )
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
            customer_rfq_id=customer_rfq_id,
            commodity_code_id=commodity_code_id,
            dangerous_good_id=dangerous_good_id,
            incoterm=rule,
            incoterms_version=version,
            trade_side=side,
            named_place=place,
        )
        self.rows.append(row)
        return row

    async def set_noted_credit_review(
        self,
        quotation_id: UUID,
        credit_review_id: UUID,
    ) -> Quotation:
        for row in self.rows:
            if row.id == quotation_id:
                row.noted_credit_review_id = credit_review_id
                return row
        raise ResourceNotFound("nieznana wycena")

    async def set_negotiated_channel_quote(
        self,
        quotation_id: UUID,
        channel_quote_id: UUID,
    ) -> Quotation:
        for row in self.rows:
            if row.id == quotation_id:
                row.negotiated_channel_quote_id = channel_quote_id
                return row
        raise ResourceNotFound("nieznana wycena")

    async def quote_batch_from_current_rates(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        charge_codes: list[str],
        origin_port_id: UUID | None,
        destination_port_id: UUID | None,
        party_id: UUID | None,
        customer_rfq_id: UUID | None = None,
        commodity_code_id: UUID | None = None,
        dangerous_good_id: UUID | None = None,
        incoterm: object = None,
        incoterms_version: object = None,
        trade_side: object = None,
        named_place: object = None,
    ) -> list[Quotation]:
        quoted: list[Quotation] = []
        for code in charge_codes:
            quoted.append(
                await self.quote_from_current_rate(
                    organization_id=organization_id,
                    user_id=user_id,
                    charge_code=code,
                    origin_port_id=origin_port_id,
                    destination_port_id=destination_port_id,
                    party_id=party_id,
                    customer_rfq_id=customer_rfq_id,
                    commodity_code_id=commodity_code_id,
                    dangerous_good_id=dangerous_good_id,
                    incoterm=incoterm,
                    incoterms_version=incoterms_version,
                    trade_side=trade_side,
                    named_place=named_place,
                )
            )
        return quoted


class StubChannelQuoteService:
    fail_get = False

    def __init__(self, session: object) -> None:
        self._session = session

    async def get_quote(self, quote_id: UUID) -> object:
        if type(self).fail_get:
            raise UnknownChannelQuote(f"nieznana oferta kanału: {quote_id}")
        return object()


class StubPartyService:
    fail_review = False

    def __init__(self, session: object) -> None:
        self._session = session

    async def get_review(self, review_id: UUID) -> object:
        if type(self).fail_review:
            raise UnknownCreditReview(f"nieznana recenzja kredytowa: {review_id}")
        return object()


@pytest.fixture
def quotations_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    stub = StubQuotationService(object())
    StubChannelQuoteService.fail_get = False
    StubPartyService.fail_review = False

    def _factory(session: object) -> StubQuotationService:
        return stub

    def _channel_factory(session: object) -> StubChannelQuoteService:
        return StubChannelQuoteService(session)

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.quotations.QuotationService", _factory)
    monkeypatch.setattr("app.api.quotations.ChannelQuoteService", _channel_factory)
    monkeypatch.setattr(
        "app.api.quotations.PartyService",
        lambda session: StubPartyService(session),
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    set_authz_checker(None)
    StubChannelQuoteService.fail_get = False
    StubPartyService.fail_review = False


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


def test_http_negotiate_saves_pointer(quotations_client: TestClient) -> None:
    headers = bearer_auth_headers()
    created = quotations_client.post(
        "/api/v1/quotations",
        headers=headers,
        json=_lane_body("THC"),
    )
    assert created.status_code == 201
    quote_id = uuid4()
    response = quotations_client.patch(
        f"/api/v1/quotations/{created.json()['id']}/negotiate",
        headers=headers,
        json={"channel_quote_id": str(quote_id)},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["negotiated_channel_quote_id"] == str(quote_id)
    assert body["amount"] == "10.5000"
    assert body["currency"] == "EUR"


def test_http_negotiate_unknown_channel(quotations_client: TestClient) -> None:
    headers = bearer_auth_headers()
    created = quotations_client.post(
        "/api/v1/quotations",
        headers=headers,
        json=_lane_body("THC"),
    )
    StubChannelQuoteService.fail_get = True
    response = quotations_client.patch(
        f"/api/v1/quotations/{created.json()['id']}/negotiate",
        headers=headers,
        json={"channel_quote_id": str(uuid4())},
    )
    assert response.status_code == 400
    assert "nieznana oferta" in response.json()["detail"]


def test_http_note_risk_saves_pointer(quotations_client: TestClient) -> None:
    headers = bearer_auth_headers()
    created = quotations_client.post(
        "/api/v1/quotations",
        headers=headers,
        json=_lane_body("THC"),
    )
    review_id = uuid4()
    response = quotations_client.patch(
        f"/api/v1/quotations/{created.json()['id']}/note-risk",
        headers=headers,
        json={"credit_review_id": str(review_id)},
    )
    assert response.status_code == 200
    assert response.json()["noted_credit_review_id"] == str(review_id)
    assert response.json()["amount"] == "10.5000"


def test_http_note_risk_unknown_review(quotations_client: TestClient) -> None:
    headers = bearer_auth_headers()
    created = quotations_client.post(
        "/api/v1/quotations",
        headers=headers,
        json=_lane_body("THC"),
    )
    StubPartyService.fail_review = True
    response = quotations_client.patch(
        f"/api/v1/quotations/{created.json()['id']}/note-risk",
        headers=headers,
        json={"credit_review_id": str(uuid4())},
    )
    assert response.status_code == 400
    assert "recenzja" in response.json()["detail"]


def test_http_negotiate_unknown_quotation(quotations_client: TestClient) -> None:
    response = quotations_client.patch(
        f"/api/v1/quotations/{uuid4()}/negotiate",
        headers=bearer_auth_headers(),
        json={"channel_quote_id": str(uuid4())},
    )
    assert response.status_code == 404


def test_http_negotiate_rejects_amount(quotations_client: TestClient) -> None:
    response = quotations_client.patch(
        f"/api/v1/quotations/{uuid4()}/negotiate",
        headers=bearer_auth_headers(),
        json={"channel_quote_id": str(uuid4()), "amount": "99.0000"},
    )
    assert response.status_code == 422


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


def test_http_quote_batch_two_codes(quotations_client: TestClient) -> None:
    origin = uuid4()
    destination = uuid4()
    party = uuid4()
    response = quotations_client.post(
        "/api/v1/quotations/batch",
        headers=bearer_auth_headers(),
        json={
            "charge_codes": ["THC", "BAF"],
            "origin_port_id": str(origin),
            "destination_port_id": str(destination),
            "party_id": str(party),
        },
    )
    assert response.status_code == 201
    rows = response.json()
    assert [row["charge_code"] for row in rows] == ["THC", "BAF"]
    assert all(row["amount"] == "10.5000" for row in rows)
    assert "buy_amount" not in rows[0]


def test_http_quote_batch_rejects_empty_list(quotations_client: TestClient) -> None:
    response = quotations_client.post(
        "/api/v1/quotations/batch",
        headers=bearer_auth_headers(),
        json={
            "charge_codes": [],
            "origin_port_id": str(uuid4()),
            "destination_port_id": str(uuid4()),
            "party_id": str(uuid4()),
        },
    )
    assert response.status_code == 422


def test_http_quote_batch_rejects_amount(quotations_client: TestClient) -> None:
    response = quotations_client.post(
        "/api/v1/quotations/batch",
        headers=bearer_auth_headers(),
        json={
            "charge_codes": ["THC"],
            "origin_port_id": str(uuid4()),
            "destination_port_id": str(uuid4()),
            "party_id": str(uuid4()),
            "amount": "99.0000",
        },
    )
    assert response.status_code == 422


def test_http_quote_batch_gap_returns_400(quotations_client: TestClient) -> None:
    response = quotations_client.post(
        "/api/v1/quotations/batch",
        headers=bearer_auth_headers(),
        json={
            "charge_codes": ["THC", "GAP"],
            "origin_port_id": str(uuid4()),
            "destination_port_id": str(uuid4()),
            "party_id": str(uuid4()),
        },
    )
    assert response.status_code == 400


def test_http_unknown_incoterm_is_400(quotations_client: TestClient) -> None:
    response = quotations_client.post(
        "/api/v1/quotations",
        headers=bearer_auth_headers(),
        json={
            **_lane_body(),
            "incoterm": "FOOBAR",
            "incoterms_version": "2020",
            "trade_side": "import",
        },
    )
    assert response.status_code == 400
    assert "incoterm" in response.json()["detail"]


def test_http_dap_without_named_place_is_409(quotations_client: TestClient) -> None:
    response = quotations_client.post(
        "/api/v1/quotations",
        headers=bearer_auth_headers(),
        json={
            **_lane_body(),
            "incoterm": "DAP",
            "incoterms_version": "2020",
            "trade_side": "import",
        },
    )
    assert response.status_code == 409
    assert "named_place" in response.json()["detail"]


def test_http_quote_keeps_amount_from_stub_not_incoterm(
    quotations_client: TestClient,
) -> None:
    created = quotations_client.post(
        "/api/v1/quotations",
        headers=bearer_auth_headers(),
        json={
            **_lane_body(),
            "incoterm": "FOB",
            "incoterms_version": "2020",
            "trade_side": "export",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["incoterm"] == "FOB"
    assert body["amount"] == "10.5000"
