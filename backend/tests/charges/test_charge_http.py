from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.charge import margin
from app.domain.errors import InvalidSourceRef, MixedCurrencyCharge, UnknownChargeCode
from app.domain.money import Money
from app.domain.organization_setting import (
    normalize_fx_rate_basis,
    normalize_fx_rate_offset_days,
    normalize_fx_rate_table,
    optional_fx_token,
)
from app.main import app
from app.models.charge import Charge, ShipmentTreeMargin
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


class StubChargeService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[Charge] = []
        self.tree_rows: list[ShipmentTreeMargin] = []

    async def list_charges(self) -> list[tuple[Charge, Decimal]]:
        return [(row, row.sell_amount - row.buy_amount) for row in self.rows]

    async def list_tree_margins(self) -> list[ShipmentTreeMargin]:
        return self.tree_rows

    async def sell_in_pln(self, *, charge_id: UUID, on_date: object) -> Decimal:
        from datetime import date as date_cls

        from app.domain.errors import InvalidNbpRate, ResourceNotFound

        if type(on_date) is not date_cls:
            raise InvalidNbpRate("kurs: data musi być dniem")
        for row in self.rows:
            if row.id == charge_id:
                if row.sell_currency == "PLN":
                    return row.sell_amount
                raise InvalidNbpRate("kurs: brak kursu NBP na dzień")
        raise ResourceNotFound("nieznana opłata")

    async def create_charge(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        charge_code: str,
        buy_amount: object,
        buy_currency: object,
        sell_amount: object,
        sell_currency: object,
        rate_line_id: UUID | None,
        source_ref: object,
        shipment_id: UUID | None = None,
        fx_rate_basis: object | None = None,
        fx_rate_offset_days: object | None = None,
        fx_rate_table: object | None = None,
    ) -> Charge:
        if isinstance(buy_amount, float) or isinstance(sell_amount, float):
            raise MixedCurrencyCharge("kwota nie może być float")
        if type(source_ref) is not str or source_ref.strip() == "":
            raise InvalidSourceRef("source_ref jest obowiązkowy")
        buy = Money.of(buy_amount, buy_currency)
        sell = Money.of(sell_amount, sell_currency)
        margin(buy, sell)
        if charge_code.strip().upper() == "LOOSE":
            raise UnknownChargeCode("nieznany kod opłaty: LOOSE")
        basis = optional_fx_token(fx_rate_basis, normalize_fx_rate_basis)
        offset = optional_fx_token(fx_rate_offset_days, normalize_fx_rate_offset_days)
        table = optional_fx_token(fx_rate_table, normalize_fx_rate_table)
        row = Charge(
            id=uuid4(),
            organization_id=organization_id,
            charge_code=charge_code.strip().upper(),
            buy_amount=buy.amount,
            buy_currency=buy.currency.code,
            sell_amount=sell.amount,
            sell_currency=sell.currency.code,
            rate_line_id=rate_line_id,
            shipment_id=shipment_id,
            fx_rate_basis=basis,
            fx_rate_offset_days=offset,
            fx_rate_table=table,
            source_ref=source_ref.strip(),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


class StubMarginFloorRepository:
    def __init__(self, session: object) -> None:
        self._session = session
        self.floor: object | None = None
        self.calls: list[dict[str, str]] = []

    async def find_for_lane(
        self,
        *,
        origin_unlocode: str,
        destination_unlocode: str,
        floor_currency: str,
    ) -> object | None:
        self.calls.append(
            {
                "origin_unlocode": origin_unlocode,
                "destination_unlocode": destination_unlocode,
                "floor_currency": floor_currency,
            }
        )
        return self.floor


class StubOperatorDecisionService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.pending_by_floor: dict[UUID, object] = {}
        self.decisions: dict[UUID, object] = {}
        self.create_calls = 0

    async def create_decision(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        subject_kind: str,
        subject_id: UUID,
        source_ref: str,
    ) -> object:
        self.create_calls += 1
        from app.domain.errors import OperatorDecisionConflict

        if subject_id in self.pending_by_floor:
            raise OperatorDecisionConflict("pending na ten subject już istnieje")
        row = SimpleNamespace(
            id=uuid4(),
            subject_kind=subject_kind,
            subject_id=subject_id,
            status="pending",
            source_ref=source_ref,
            organization_id=organization_id,
            created_by=user_id,
        )
        self.pending_by_floor[subject_id] = row
        self.decisions[row.id] = row
        return row

    async def get_pending(self, subject_kind: str, subject_id: UUID) -> object | None:
        row = self.pending_by_floor.get(subject_id)
        if row is None:
            return None
        if row.subject_kind != subject_kind or row.status != "pending":
            return None
        return row

    async def get_decision(self, decision_id: UUID) -> object:
        from app.domain.errors import ResourceNotFound

        found = self.decisions.get(decision_id)
        if found is None:
            raise ResourceNotFound(f"nieznana decyzja operatora: {decision_id}")
        return found


@pytest.fixture
def charges_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    stub = StubChargeService(object())
    floor_stub = StubMarginFloorRepository(object())
    decision_stub = StubOperatorDecisionService(object())

    def _factory(session: object) -> StubChargeService:
        return stub

    def _floor_factory(session: object) -> StubMarginFloorRepository:
        return floor_stub

    def _decision_factory(session: object) -> StubOperatorDecisionService:
        return decision_stub

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.charges.ChargeService", _factory)
    monkeypatch.setattr("app.api.charges.MarginFloorRepository", _floor_factory)
    monkeypatch.setattr("app.api.charges.OperatorDecisionService", _decision_factory)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    client = TestClient(app)
    client.floor_stub = floor_stub  # type: ignore[attr-defined]
    client.decision_stub = decision_stub  # type: ignore[attr-defined]
    client.charge_stub = stub  # type: ignore[attr-defined]
    yield client
    app.dependency_overrides.clear()
    set_authz_checker(None)
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_charge_stores_fx_rate(charges_client: TestClient) -> None:
    org_id = uuid4()
    reply = charges_client.post(
        "/api/v1/charges",
        headers=bearer_auth_headers(organization_id=org_id),
        json={
            "charge_code": "THC",
            "buy_amount": "10",
            "buy_currency": "EUR",
            "sell_amount": "14",
            "sell_currency": "EUR",
            "source_ref": "tenant:manual",
            "fx_rate_basis": "etd",
            "fx_rate_offset_days": "-1",
            "fx_rate_table": "nbp_a",
        },
    )
    assert reply.status_code == 201
    body = reply.json()
    assert body["fx_rate_basis"] == "etd"
    assert body["fx_rate_offset_days"] == "-1"
    assert body["fx_rate_table"] == "nbp_a"


def test_http_rejects_bad_fx_rate_basis(charges_client: TestClient) -> None:
    reply = charges_client.post(
        "/api/v1/charges",
        headers=bearer_auth_headers(),
        json={
            "charge_code": "THC",
            "buy_amount": "10",
            "buy_currency": "EUR",
            "sell_amount": "14",
            "sell_currency": "EUR",
            "source_ref": "tenant:manual",
            "fx_rate_basis": "tomorrow",
        },
    )
    assert reply.status_code == 400
    assert "kurs" in reply.json()["detail"]


def test_http_lists_tree_margin(charges_client: TestClient) -> None:
    org_id = uuid4()
    shipment_id = uuid4()
    charges_client.charge_stub.tree_rows = [  # type: ignore[attr-defined]
        ShipmentTreeMargin(
            organization_id=org_id,
            shipment_id=shipment_id,
            currency="EUR",
            buy_amount=Decimal("12.0000"),
            sell_amount=Decimal("19.0000"),
            margin_amount=Decimal("7.0000"),
            charge_count=2,
        ),
    ]
    reply = charges_client.get(
        "/api/v1/charges/tree-margins",
        headers=bearer_auth_headers(organization_id=org_id),
    )
    assert reply.status_code == 200
    body = reply.json()
    assert body[0]["shipment_id"] == str(shipment_id)
    assert body[0]["currency"] == "EUR"
    assert body[0]["margin_amount"] == "7.0000"
    assert body[0]["charge_count"] == 2


def test_http_sell_in_pln_for_pln_charge(charges_client: TestClient) -> None:
    org_id = uuid4()
    user_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id, user_id=user_id)
    created = charges_client.post(
        "/api/v1/charges",
        headers=headers,
        json={
            "charge_code": "THC",
            "buy_amount": "10.0000",
            "buy_currency": "PLN",
            "sell_amount": "14.0000",
            "sell_currency": "PLN",
            "source_ref": "fixture://charge/pln",
        },
    )
    assert created.status_code == 201
    charge_id = created.json()["id"]
    reply = charges_client.get(
        f"/api/v1/charges/{charge_id}/sell-in-pln",
        headers=headers,
        params={"on_date": "2026-09-01"},
    )
    assert reply.status_code == 200
    body = reply.json()
    assert body["charge_id"] == charge_id
    assert body["on_date"] == "2026-09-01"
    assert body["sell_amount_pln"] == "14.0000"
    assert body["currency"] == "PLN"


def test_http_sell_in_pln_missing_rate_is_kurs(charges_client: TestClient) -> None:
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = charges_client.post(
        "/api/v1/charges",
        headers=headers,
        json={
            "charge_code": "THC",
            "buy_amount": "10.0000",
            "buy_currency": "EUR",
            "sell_amount": "14.0000",
            "sell_currency": "EUR",
            "source_ref": "fixture://charge/eur",
        },
    )
    assert created.status_code == 201
    charge_id = created.json()["id"]
    reply = charges_client.get(
        f"/api/v1/charges/{charge_id}/sell-in-pln",
        headers=headers,
        params={"on_date": "2026-09-01"},
    )
    assert reply.status_code == 400
    assert "kurs" in reply.json()["detail"]


def test_http_create_and_list_charges(charges_client: TestClient) -> None:
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = charges_client.post(
        "/api/v1/charges",
        headers=headers,
        json={
            "charge_code": "THC",
            "buy_amount": "10.5",
            "buy_currency": "EUR",
            "sell_amount": "14",
            "sell_currency": "EUR",
            "source_ref": "tenant:manual",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["charge_code"] == "THC"
    assert body["buy_amount"] == "10.5000"
    assert body["sell_amount"] == "14.0000"
    assert body["margin_amount"] == "3.5000"
    assert body["margin_currency"] == "EUR"
    assert body["buy_currency"] == "EUR"
    assert body["organization_id"] == str(org_id)
    assert body["rate_line_id"] is None
    assert body["shipment_id"] is None
    assert body["source_ref"] == "tenant:manual"
    assert isinstance(body["margin_amount"], str)

    listed = charges_client.get("/api/v1/charges", headers=headers)
    assert listed.status_code == 200
    rows = listed.json()
    assert len(rows) == 1
    assert rows[0]["id"] == body["id"]
    assert rows[0]["margin_amount"] == "3.5000"
    assert rows[0]["shipment_id"] is None


def test_http_create_charge_stores_shipment_id(charges_client: TestClient) -> None:
    shipment_id = uuid4()
    headers = bearer_auth_headers()
    created = charges_client.post(
        "/api/v1/charges",
        headers=headers,
        json={
            "charge_code": "THC",
            "buy_amount": "10",
            "buy_currency": "EUR",
            "sell_amount": "14",
            "sell_currency": "EUR",
            "source_ref": "tenant:manual",
            "shipment_id": str(shipment_id),
        },
    )
    assert created.status_code == 201
    assert created.json()["shipment_id"] == str(shipment_id)


def test_http_rejects_bad_shipment_id(charges_client: TestClient) -> None:
    headers = bearer_auth_headers()
    reply = charges_client.post(
        "/api/v1/charges",
        headers=headers,
        json={
            "charge_code": "THC",
            "buy_amount": "10",
            "buy_currency": "EUR",
            "sell_amount": "14",
            "sell_currency": "EUR",
            "source_ref": "tenant:manual",
            "shipment_id": "nie-uuid",
        },
    )
    assert reply.status_code == 422


def test_http_rejects_mixed_currency(charges_client: TestClient) -> None:
    response = charges_client.post(
        "/api/v1/charges",
        headers=bearer_auth_headers(),
        json={
            "charge_code": "THC",
            "buy_amount": "10",
            "buy_currency": "EUR",
            "sell_amount": "14",
            "sell_currency": "USD",
            "source_ref": "tenant:manual",
        },
    )
    assert response.status_code == 400
    assert "walutę" in response.json()["detail"]


def test_http_rejects_numeric_buy_amount(charges_client: TestClient) -> None:
    response = charges_client.post(
        "/api/v1/charges",
        headers=bearer_auth_headers(),
        json={
            "charge_code": "THC",
            "buy_amount": 10.5,
            "buy_currency": "EUR",
            "sell_amount": "14",
            "sell_currency": "EUR",
            "source_ref": "tenant:manual",
        },
    )
    assert response.status_code == 422


def test_http_rejects_unknown_charge_code(charges_client: TestClient) -> None:
    response = charges_client.post(
        "/api/v1/charges",
        headers=bearer_auth_headers(),
        json={
            "charge_code": "LOOSE",
            "buy_amount": "10",
            "buy_currency": "EUR",
            "sell_amount": "14",
            "sell_currency": "EUR",
            "source_ref": "tenant:manual",
        },
    )
    assert response.status_code == 400
    assert "LOOSE" in response.json()["detail"]


def test_http_rejects_blank_source_ref(charges_client: TestClient) -> None:
    response = charges_client.post(
        "/api/v1/charges",
        headers=bearer_auth_headers(),
        json={
            "charge_code": "THC",
            "buy_amount": "10",
            "buy_currency": "EUR",
            "sell_amount": "14",
            "sell_currency": "EUR",
            "source_ref": "   ",
        },
    )
    assert response.status_code == 400
    assert "source_ref" in response.json()["detail"]


def test_http_rejects_margin_below_floor(charges_client: TestClient) -> None:
    floor_id = uuid4()
    floor_stub: StubMarginFloorRepository = charges_client.floor_stub  # type: ignore[attr-defined]
    decision_stub: StubOperatorDecisionService = charges_client.decision_stub  # type: ignore[attr-defined]
    floor_stub.floor = SimpleNamespace(
        id=floor_id,
        floor_amount=Decimal("10.0000"),
        floor_currency="EUR",
    )
    response = charges_client.post(
        "/api/v1/charges",
        headers=bearer_auth_headers(),
        json={
            "charge_code": "THC",
            "buy_amount": "10",
            "buy_currency": "EUR",
            "sell_amount": "14",
            "sell_currency": "EUR",
            "source_ref": "tenant:manual",
            "origin_unlocode": "PLGDN",
            "destination_unlocode": "DEHAM",
        },
    )
    assert response.status_code == 409
    body = response.json()
    assert "podłogi" in body["detail"]
    assert body["decision_id"] == str(decision_stub.pending_by_floor[floor_id].id)
    assert decision_stub.create_calls == 1
    assert floor_stub.calls == [
        {
            "origin_unlocode": "PLGDN",
            "destination_unlocode": "DEHAM",
            "floor_currency": "EUR",
        }
    ]


def test_http_reuses_pending_floor_decision(charges_client: TestClient) -> None:
    floor_id = uuid4()
    floor_stub: StubMarginFloorRepository = charges_client.floor_stub  # type: ignore[attr-defined]
    decision_stub: StubOperatorDecisionService = charges_client.decision_stub  # type: ignore[attr-defined]
    floor_stub.floor = SimpleNamespace(
        id=floor_id,
        floor_amount=Decimal("10.0000"),
        floor_currency="EUR",
    )
    payload = {
        "charge_code": "THC",
        "buy_amount": "10",
        "buy_currency": "EUR",
        "sell_amount": "14",
        "sell_currency": "EUR",
        "source_ref": "tenant:manual",
        "origin_unlocode": "PLGDN",
        "destination_unlocode": "DEHAM",
    }
    first = charges_client.post(
        "/api/v1/charges",
        headers=bearer_auth_headers(),
        json=payload,
    )
    second = charges_client.post(
        "/api/v1/charges",
        headers=bearer_auth_headers(),
        json=payload,
    )
    assert first.status_code == 409
    assert second.status_code == 409
    assert first.json()["decision_id"] == second.json()["decision_id"]
    assert decision_stub.create_calls == 2


def test_http_accepts_below_floor_with_accepted_decision(
    charges_client: TestClient,
) -> None:
    floor_id = uuid4()
    decision_id = uuid4()
    floor_stub: StubMarginFloorRepository = charges_client.floor_stub  # type: ignore[attr-defined]
    decision_stub: StubOperatorDecisionService = charges_client.decision_stub  # type: ignore[attr-defined]
    floor_stub.floor = SimpleNamespace(
        id=floor_id,
        floor_amount=Decimal("10.0000"),
        floor_currency="EUR",
    )
    decision_stub.decisions[decision_id] = SimpleNamespace(
        id=decision_id,
        subject_kind="margin_floor",
        subject_id=floor_id,
        status="accepted",
    )
    response = charges_client.post(
        "/api/v1/charges",
        headers=bearer_auth_headers(),
        json={
            "charge_code": "THC",
            "buy_amount": "10",
            "buy_currency": "EUR",
            "sell_amount": "14",
            "sell_currency": "EUR",
            "source_ref": "tenant:manual",
            "origin_unlocode": "PLGDN",
            "destination_unlocode": "DEHAM",
            "floor_decision_id": str(decision_id),
        },
    )
    assert response.status_code == 201
    assert response.json()["margin_amount"] == "4.0000"
    assert decision_stub.create_calls == 0


def test_http_rejects_pending_floor_decision_override(
    charges_client: TestClient,
) -> None:
    floor_id = uuid4()
    decision_id = uuid4()
    floor_stub: StubMarginFloorRepository = charges_client.floor_stub  # type: ignore[attr-defined]
    decision_stub: StubOperatorDecisionService = charges_client.decision_stub  # type: ignore[attr-defined]
    floor_stub.floor = SimpleNamespace(
        id=floor_id,
        floor_amount=Decimal("10.0000"),
        floor_currency="EUR",
    )
    decision_stub.decisions[decision_id] = SimpleNamespace(
        id=decision_id,
        subject_kind="margin_floor",
        subject_id=floor_id,
        status="pending",
    )
    response = charges_client.post(
        "/api/v1/charges",
        headers=bearer_auth_headers(),
        json={
            "charge_code": "THC",
            "buy_amount": "10",
            "buy_currency": "EUR",
            "sell_amount": "14",
            "sell_currency": "EUR",
            "source_ref": "tenant:manual",
            "origin_unlocode": "PLGDN",
            "destination_unlocode": "DEHAM",
            "floor_decision_id": str(decision_id),
        },
    )
    assert response.status_code == 400
    assert "accepted" in response.json()["detail"]


def test_http_accepts_margin_at_or_above_floor(charges_client: TestClient) -> None:
    floor_stub: StubMarginFloorRepository = charges_client.floor_stub  # type: ignore[attr-defined]
    floor_stub.floor = SimpleNamespace(
        id=uuid4(),
        floor_amount=Decimal("3.5000"),
        floor_currency="EUR",
    )
    response = charges_client.post(
        "/api/v1/charges",
        headers=bearer_auth_headers(),
        json={
            "charge_code": "THC",
            "buy_amount": "10",
            "buy_currency": "EUR",
            "sell_amount": "14",
            "sell_currency": "EUR",
            "source_ref": "tenant:manual",
            "origin_unlocode": "plgdn",
            "destination_unlocode": "deham",
        },
    )
    assert response.status_code == 201
    assert response.json()["margin_amount"] == "4.0000"


def test_http_skips_floor_when_lane_omitted(charges_client: TestClient) -> None:
    floor_stub: StubMarginFloorRepository = charges_client.floor_stub  # type: ignore[attr-defined]
    floor_stub.floor = object()
    response = charges_client.post(
        "/api/v1/charges",
        headers=bearer_auth_headers(),
        json={
            "charge_code": "THC",
            "buy_amount": "10",
            "buy_currency": "EUR",
            "sell_amount": "11",
            "sell_currency": "EUR",
            "source_ref": "tenant:manual",
        },
    )
    assert response.status_code == 201
    assert floor_stub.calls == []


def test_http_rejects_incomplete_floor_lane(charges_client: TestClient) -> None:
    response = charges_client.post(
        "/api/v1/charges",
        headers=bearer_auth_headers(),
        json={
            "charge_code": "THC",
            "buy_amount": "10",
            "buy_currency": "EUR",
            "sell_amount": "14",
            "sell_currency": "EUR",
            "source_ref": "tenant:manual",
            "origin_unlocode": "PLGDN",
        },
    )
    assert response.status_code == 400
    assert "obu końców" in response.json()["detail"]
