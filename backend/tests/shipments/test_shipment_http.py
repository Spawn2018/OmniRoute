from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import InvalidShipment, ResourceNotFound, ShipmentConflict
from app.domain.shipment import (
    require_parent_pair,
    require_parent_shipment_id,
    require_relation_kind,
    require_shipment_ref,
)
from app.main import app
from app.models.quotation import Quotation
from app.models.shipment import Shipment
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
            raise ResourceNotFound(f"nieznana wycena: {quotation_id}")
        return self.row


class StubShipmentService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[Shipment] = []

    async def list_shipments(self) -> list[Shipment]:
        return list(self.rows)

    async def create_shipment(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        quotation_id: UUID,
        party_id: UUID,
        source_ref: str,
        shipment_ref: object = None,
        parent_shipment_id: object = None,
        relation_kind: object = None,
        guide_code: object = None,
        plant_label: object = None,
        carrier_label: object = None,
    ) -> Shipment:
        if any(row.quotation_id == quotation_id for row in self.rows):
            raise ShipmentConflict("to zlecenie już istnieje dla tej wyceny")
        if source_ref.strip() == "":
            raise InvalidShipment("wskazanie zapisu zlecenia")
        row_id = uuid4()
        parent = require_parent_shipment_id(parent_shipment_id)
        kind = require_relation_kind(relation_kind)
        require_parent_pair(parent, kind, child_id=row_id)
        token = None
        if type(guide_code) is str:
            stripped = guide_code.strip()
            token = stripped or None
        plant = None
        if type(plant_label) is str:
            plant = plant_label.strip() or None
        carrier = None
        if type(carrier_label) is str:
            carrier = carrier_label.strip() or None
        row = Shipment(
            id=row_id,
            organization_id=organization_id,
            quotation_id=quotation_id,
            party_id=party_id,
            source_ref=source_ref,
            shipment_ref=require_shipment_ref(shipment_ref),
            parent_shipment_id=parent,
            relation_kind=kind,
            guide_code=token,
            plant_label=plant,
            carrier_label=carrier,
            status="draft",
            created_by=user_id,
        )
        self.rows.append(row)
        return row


class _GuideDesk:
    def __init__(self, codes: list[str]) -> None:
        self._codes = codes
        self._lanes: dict[str, str | None] = {}
        self._modes: dict[str, str | None] = {}

    async def list_guides(self) -> list[object]:
        return [
            type(
                "G",
                (),
                {
                    "guide_code": code,
                    "lane_label": self._lanes.get(code),
                    "mode_label": self._modes.get(code),
                },
            )()
            for code in self._codes
        ]


class _EnforcementDesk:
    def __init__(self, kinds: list[str]) -> None:
        self._kinds = kinds

    async def list_marks(self) -> list[object]:
        return [type("E", (), {"enforcement_kind": kind})() for kind in self._kinds]


class _MatchDesk:
    def __init__(self, kinds: list[str]) -> None:
        self._kinds = kinds

    async def list_marks(self) -> list[object]:
        return [type("M", (), {"match_kind": kind})() for kind in self._kinds]


def _quote(*, party_id: UUID | None) -> Quotation:
    from decimal import Decimal

    return Quotation(
        id=uuid4(),
        organization_id=uuid4(),
        charge_code="THC",
        rate_line_id=uuid4(),
        amount=Decimal("10.0000"),
        currency="EUR",
        source_ref="tariff://a",
        party_id=party_id,
    )


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    quotes = StubQuotationService(object())
    shipments = StubShipmentService(object())
    guides = _GuideDesk([])
    enforcements = _EnforcementDesk([])
    matches = _MatchDesk([])

    def _quotes(_session: object) -> StubQuotationService:
        return quotes

    def _shipments(_session: object) -> StubShipmentService:
        return shipments

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.shipments.QuotationService", _quotes)
    monkeypatch.setattr("app.api.shipments.ShipmentService", _shipments)
    monkeypatch.setattr("app.api.shipments.RoutingGuideService", lambda _s: guides)
    monkeypatch.setattr(
        "app.api.shipments.RoutingGuideEnforcementService",
        lambda _s: enforcements,
    )
    monkeypatch.setattr(
        "app.api.shipments.RoutingGuideMatchService",
        lambda _s: matches,
    )
    quotes.row = _quote(party_id=uuid4())
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), quotes, shipments, guides, enforcements, matches
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_shipment(catalog_client: object) -> None:
    client, quotes, _shipments, _guides, _enf, _matches = catalog_client
    assert quotes.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/shipments",
        headers=headers,
        json={
            "quotation_id": str(quotes.row.id),
            "source_ref": "fixture://shipment/1",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["quotation_id"] == str(quotes.row.id)
    assert body["party_id"] == str(quotes.row.party_id)
    assert body["source_ref"] == "fixture://shipment/1"
    assert body["shipment_ref"] is None
    assert body["parent_shipment_id"] is None
    assert body["relation_kind"] is None
    assert body["status"] == "draft"
    assert "amount" not in body
    assert "margin" not in body

    listed = client.get("/api/v1/shipments", headers=headers)
    assert listed.status_code == 200
    rows = listed.json()
    assert len(rows) == 1
    assert rows[0]["id"] == body["id"]


def test_http_create_shipment_unknown_quotation_is_404(catalog_client: object) -> None:
    client, _quotes, _shipments, _guides, _enf, _matches = catalog_client
    response = client.post(
        "/api/v1/shipments",
        headers=bearer_auth_headers(),
        json={
            "quotation_id": str(uuid4()),
            "source_ref": "fixture://shipment/1",
        },
    )
    assert response.status_code == 404


def test_http_create_shipment_without_party_is_400(catalog_client: object) -> None:
    client, quotes, _shipments, _guides, _enf, _matches = catalog_client
    quotes.row = _quote(party_id=None)
    response = client.post(
        "/api/v1/shipments",
        headers=bearer_auth_headers(),
        json={
            "quotation_id": str(quotes.row.id),
            "source_ref": "fixture://shipment/1",
        },
    )
    assert response.status_code == 400
    assert "kontrahenta" in response.json()["detail"]


def test_http_duplicate_shipment_for_quotation_is_conflict(catalog_client: object) -> None:
    client, quotes, _shipments, _guides, _enf, _matches = catalog_client
    assert quotes.row is not None
    headers = bearer_auth_headers()
    payload = {
        "quotation_id": str(quotes.row.id),
        "source_ref": "fixture://shipment/1",
    }
    first = client.post("/api/v1/shipments", headers=headers, json=payload)
    assert first.status_code == 201
    second = client.post("/api/v1/shipments", headers=headers, json=payload)
    assert second.status_code == 400
    assert "już istnieje" in second.json()["detail"]


def test_http_create_shipment_with_ref(catalog_client: object) -> None:
    client, quotes, _shipments, _guides, _enf, _matches = catalog_client
    assert quotes.row is not None
    created = client.post(
        "/api/v1/shipments",
        headers=bearer_auth_headers(),
        json={
            "quotation_id": str(quotes.row.id),
            "source_ref": "fixture://shipment/1",
            "shipment_ref": "omni://shipment/ab1",
        },
    )
    assert created.status_code == 201
    assert created.json()["shipment_ref"] == "omni://shipment/ab1"
    assert "qr" not in created.json()


def test_http_create_shipment_bad_ref_is_400(catalog_client: object) -> None:
    client, quotes, _shipments, _guides, _enf, _matches = catalog_client
    assert quotes.row is not None
    numbered = client.post(
        "/api/v1/shipments",
        headers=bearer_auth_headers(),
        json={
            "quotation_id": str(quotes.row.id),
            "source_ref": "fixture://shipment/1",
            "shipment_ref": "omni://shipment/",
        },
    )
    assert numbered.status_code == 400
    assert "numer" in numbered.json()["detail"]
    foreign = client.post(
        "/api/v1/shipments",
        headers=bearer_auth_headers(),
        json={
            "quotation_id": str(quotes.row.id),
            "source_ref": "fixture://shipment/1",
            "shipment_ref": "http://print.example/x",
        },
    )
    assert foreign.status_code == 400
    assert "obce" in foreign.json()["detail"]


def test_http_create_shipment_with_parent(catalog_client: object) -> None:
    client, quotes, _shipments, _guides, _enf, _matches = catalog_client
    assert quotes.row is not None
    parent_id = uuid4()
    created = client.post(
        "/api/v1/shipments",
        headers=bearer_auth_headers(),
        json={
            "quotation_id": str(quotes.row.id),
            "source_ref": "fixture://shipment/1",
            "parent_shipment_id": str(parent_id),
            "relation_kind": "drayage",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["parent_shipment_id"] == str(parent_id)
    assert body["relation_kind"] == "drayage"
    assert "margin" not in body
    assert "charge" not in body


def test_http_create_shipment_parent_without_kind_is_400(catalog_client: object) -> None:
    client, quotes, _shipments, _guides, _enf, _matches = catalog_client
    assert quotes.row is not None
    response = client.post(
        "/api/v1/shipments",
        headers=bearer_auth_headers(),
        json={
            "quotation_id": str(quotes.row.id),
            "source_ref": "fixture://shipment/1",
            "parent_shipment_id": str(uuid4()),
        },
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_http_create_shipment_kind_without_parent_is_400(catalog_client: object) -> None:
    client, quotes, _shipments, _guides, _enf, _matches = catalog_client
    assert quotes.row is not None
    response = client.post(
        "/api/v1/shipments",
        headers=bearer_auth_headers(),
        json={
            "quotation_id": str(quotes.row.id),
            "source_ref": "fixture://shipment/1",
            "relation_kind": "drayage",
        },
    )
    assert response.status_code == 400
    assert "główne" in response.json()["detail"]


def test_http_create_shipment_bad_kind_is_400(catalog_client: object) -> None:
    client, quotes, _shipments, _guides, _enf, _matches = catalog_client
    assert quotes.row is not None
    response = client.post(
        "/api/v1/shipments",
        headers=bearer_auth_headers(),
        json={
            "quotation_id": str(quotes.row.id),
            "source_ref": "fixture://shipment/1",
            "parent_shipment_id": str(uuid4()),
            "relation_kind": "margin",
        },
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_http_block_409_rejects_shipment_without_guide(catalog_client: object) -> None:
    client, quotes, _shipments, guides, enforcements, _matches = catalog_client
    assert quotes.row is not None
    guides._codes = ["lane_pl_de"]
    enforcements._kinds = ["block_409"]
    response = client.post(
        "/api/v1/shipments",
        headers=bearer_auth_headers(),
        json={
            "quotation_id": str(quotes.row.id),
            "source_ref": "fixture://shipment/block",
        },
    )
    assert response.status_code == 409
    assert "guide_code" in response.json()["detail"]


def test_http_block_409_accepts_known_guide(catalog_client: object) -> None:
    client, quotes, _shipments, guides, enforcements, _matches = catalog_client
    assert quotes.row is not None
    guides._codes = ["lane_pl_de"]
    enforcements._kinds = ["block_409"]
    created = client.post(
        "/api/v1/shipments",
        headers=bearer_auth_headers(),
        json={
            "quotation_id": str(quotes.row.id),
            "source_ref": "fixture://shipment/ok",
            "guide_code": "lane_pl_de",
        },
    )
    assert created.status_code == 201
    assert created.json()["guide_code"] == "lane_pl_de"


def test_http_rejects_shipment_when_lane_match_fails(catalog_client: object) -> None:
    client, quotes, _shipments, guides, enforcements, matches = catalog_client
    assert quotes.row is not None
    guides._codes = ["lane_pl_de"]
    guides._lanes = {"lane_pl_de": "pl-de"}
    enforcements._kinds = ["block_409"]
    matches._kinds = ["lane_label"]
    response = client.post(
        "/api/v1/shipments",
        headers=bearer_auth_headers(),
        json={
            "quotation_id": str(quotes.row.id),
            "source_ref": "fixture://shipment/lane-bad",
            "guide_code": "lane_pl_de",
            "plant_label": "wrong",
        },
    )
    assert response.status_code == 409
    assert "plant_label" in response.json()["detail"]


def test_http_accepts_shipment_when_lane_match_ok(catalog_client: object) -> None:
    client, quotes, _shipments, guides, enforcements, matches = catalog_client
    assert quotes.row is not None
    guides._codes = ["lane_pl_de"]
    guides._lanes = {"lane_pl_de": "Gdańsk"}
    enforcements._kinds = ["block_409"]
    matches._kinds = ["lane_label"]
    created = client.post(
        "/api/v1/shipments",
        headers=bearer_auth_headers(),
        json={
            "quotation_id": str(quotes.row.id),
            "source_ref": "fixture://shipment/lane-ok",
            "guide_code": "lane_pl_de",
            "plant_label": " gdańsk ",
        },
    )
    assert created.status_code == 201
    assert created.json()["plant_label"] == "gdańsk"
