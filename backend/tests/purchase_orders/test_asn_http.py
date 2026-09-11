from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.asn import parse_asn_row
from app.domain.errors import ResourceNotFound
from app.main import app
from app.models.asn import Asn
from tests.http_auth import bearer_auth_headers

_FORBIDDEN_FIELDS = ("shipment_id", "edi", "amount", "currency", "buy_amount", "payload")


class PermitAsnAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryAsnDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.notices: list[Asn] = []
        self.known_headers: set[UUID] = set()

    async def list_notices(self) -> list[Asn]:
        return list(self.notices)

    async def get_notice(self, asn_id: UUID) -> Asn:
        for row in self.notices:
            if row.id == asn_id:
                return row
        raise ResourceNotFound("nieznane awizo")

    async def persist_asn(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        purchase_order_id: object,
        asn_code: object,
        plant_label: object,
        carrier_label: object,
        ship_ref_label: object,
        guide_code: object,
        source_ref: object,
    ) -> Asn:
        packed = parse_asn_row(
            purchase_order_id=purchase_order_id,
            asn_code=asn_code,
            plant_label=plant_label,
            carrier_label=carrier_label,
            ship_ref_label=ship_ref_label,
            guide_code=guide_code,
            source_ref=source_ref,
        )
        header = packed[0]
        if header not in self.known_headers:
            raise ResourceNotFound("nieznane zamówienie")
        row = Asn(
            id=uuid4(),
            organization_id=organization_id,
            purchase_order_id=header,
            asn_code=packed[1],
            plant_label=packed[2],
            carrier_label=packed[3],
            ship_ref_label=packed[4],
            guide_code=packed[5],
            source_ref=packed[6],
            created_by=user_id,
        )
        self.notices.append(row)
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


@pytest.fixture
def asn_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryAsnDesk(object())
    guides = _GuideDesk([])
    enforcements = _EnforcementDesk([])
    matches = _MatchDesk([])

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr("app.api.asns.AsnService", lambda _s: desk)
    monkeypatch.setattr("app.api.asns.RoutingGuideService", lambda _s: guides)
    monkeypatch.setattr(
        "app.api.asns.RoutingGuideEnforcementService",
        lambda _s: enforcements,
    )
    monkeypatch.setattr(
        "app.api.asns.RoutingGuideMatchService",
        lambda _s: matches,
    )
    set_authz_checker(PermitAsnAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk, guides, enforcements, matches
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(header: UUID, **extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "purchase_order_id": str(header),
        "asn_code": "asn_01",
        "plant_label": "Gdańsk",
        "carrier_label": "DB Schenker",
        "ship_ref_label": "REF-9",
        "source_ref": "fixture://asn/pl-1",
    }
    body.update(extra)
    return body


def test_http_lists_and_creates_asn(asn_http: object) -> None:
    client, desk, _guides, _enf, _matches = asn_http
    header = uuid4()
    desk.known_headers.add(header)
    created = client.post(
        "/api/v1/asns",
        headers=bearer_auth_headers(),
        json=_payload(header),
    )
    assert created.status_code == 201
    body = created.json()
    assert body["asn_code"] == "asn_01"
    assert body["purchase_order_id"] == str(header)
    assert body["plant_label"] == "Gdańsk"
    assert body["guide_code"] is None
    listed = client.get("/api/v1/asns", headers=bearer_auth_headers())
    assert listed.status_code == 200
    assert len(listed.json()) == 1


def test_http_creates_asn_with_known_guide_under_block_409(asn_http: object) -> None:
    client, desk, guides, enforcements, _matches = asn_http
    header = uuid4()
    desk.known_headers.add(header)
    guides._codes = ["lane_pl_de"]
    enforcements._kinds = ["block_409"]
    created = client.post(
        "/api/v1/asns",
        headers=bearer_auth_headers(),
        json=_payload(header, guide_code="lane_pl_de", asn_code="asn_02"),
    )
    assert created.status_code == 201
    assert created.json()["guide_code"] == "lane_pl_de"


def test_http_rejects_asn_without_guide_when_block_409(asn_http: object) -> None:
    client, desk, guides, enforcements, _matches = asn_http
    header = uuid4()
    desk.known_headers.add(header)
    guides._codes = ["lane_pl_de"]
    enforcements._kinds = ["block_409"]
    response = client.post(
        "/api/v1/asns",
        headers=bearer_auth_headers(),
        json=_payload(header),
    )
    assert response.status_code == 409
    assert "guide_code" in response.json()["detail"]


def test_http_rejects_unknown_guide_when_block_409(asn_http: object) -> None:
    client, desk, guides, enforcements, _matches = asn_http
    header = uuid4()
    desk.known_headers.add(header)
    guides._codes = ["lane_pl_de"]
    enforcements._kinds = ["block_409"]
    response = client.post(
        "/api/v1/asns",
        headers=bearer_auth_headers(),
        json=_payload(header, guide_code="other_lane"),
    )
    assert response.status_code == 409
    assert "katalogiem" in response.json()["detail"]


def test_http_allows_asn_without_guide_when_record_only(asn_http: object) -> None:
    client, desk, _guides, enforcements, _matches = asn_http
    header = uuid4()
    desk.known_headers.add(header)
    enforcements._kinds = ["record_only"]
    created = client.post(
        "/api/v1/asns",
        headers=bearer_auth_headers(),
        json=_payload(header, asn_code="asn_03"),
    )
    assert created.status_code == 201
    assert created.json()["guide_code"] is None


def test_http_rejects_bad_asn_code(asn_http: object) -> None:
    client, desk, _guides, _enf, _matches = asn_http
    header = uuid4()
    desk.known_headers.add(header)
    response = client.post(
        "/api/v1/asns",
        headers=bearer_auth_headers(),
        json=_payload(header, asn_code="X"),
    )
    assert response.status_code == 400
    assert "awizo" in response.json()["detail"]


def test_http_rejects_unknown_header(asn_http: object) -> None:
    client, _desk, _guides, _enf, _matches = asn_http
    response = client.post(
        "/api/v1/asns",
        headers=bearer_auth_headers(),
        json=_payload(uuid4()),
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "nieznane zamówienie"


@pytest.mark.parametrize("field", _FORBIDDEN_FIELDS)
def test_http_forbids_shipment_and_money_fields(asn_http: object, field: str) -> None:
    client, desk, _guides, _enf, _matches = asn_http
    header = uuid4()
    desk.known_headers.add(header)
    body = _payload(header)
    body[field] = "x" if field != "amount" else "1"
    response = client.post(
        "/api/v1/asns",
        headers=bearer_auth_headers(),
        json=body,
    )
    assert response.status_code == 422

def test_http_rejects_asn_when_lane_match_fails(asn_http: object) -> None:
    client, desk, guides, enforcements, matches = asn_http
    header = uuid4()
    desk.known_headers.add(header)
    guides._codes = ["lane_pl_de"]
    guides._lanes = {"lane_pl_de": "pl-de"}
    enforcements._kinds = ["block_409"]
    matches._kinds = ["lane_label"]
    response = client.post(
        "/api/v1/asns",
        headers=bearer_auth_headers(),
        json=_payload(header, guide_code="lane_pl_de", plant_label="wrong"),
    )
    assert response.status_code == 409
    assert "plant_label" in response.json()["detail"]


def test_http_accepts_asn_when_lane_match_ok(asn_http: object) -> None:
    client, desk, guides, enforcements, matches = asn_http
    header = uuid4()
    desk.known_headers.add(header)
    guides._codes = ["lane_pl_de"]
    guides._lanes = {"lane_pl_de": "Gdańsk"}
    enforcements._kinds = ["block_409"]
    matches._kinds = ["lane_label"]
    created = client.post(
        "/api/v1/asns",
        headers=bearer_auth_headers(),
        json=_payload(
            header,
            guide_code="lane_pl_de",
            asn_code="asn_lane",
            plant_label=" gdańsk ",
        ),
    )
    assert created.status_code == 201


def test_http_promote_asn_creates_shipment(asn_http: object, monkeypatch: pytest.MonkeyPatch) -> None:
    from decimal import Decimal

    from app.models.quotation import Quotation
    from app.models.shipment import Shipment

    client, desk, _guides, _enf, _matches = asn_http
    header = uuid4()
    desk.known_headers.add(header)
    created = client.post(
        "/api/v1/asns",
        headers=bearer_auth_headers(),
        json=_payload(header, guide_code=None, asn_code="asn_prom"),
    )
    assert created.status_code == 201
    asn_id = created.json()["id"]
    quote_id = uuid4()
    party_id = uuid4()
    org_id = uuid4()

    class _Quotes:
        async def get_quotation(self, quotation_id: UUID) -> Quotation:
            assert quotation_id == quote_id
            return Quotation(
                id=quote_id,
                organization_id=org_id,
                charge_code="THC",
                rate_line_id=uuid4(),
                amount=Decimal("10.0000"),
                currency="EUR",
                source_ref="tariff://a",
                party_id=party_id,
            )

    class _Shipments:
        async def create_shipment(self, **kwargs: object) -> Shipment:
            assert kwargs["asn_id"] == UUID(asn_id)
            assert kwargs["plant_label"] == "Gdańsk"
            return Shipment(
                id=uuid4(),
                organization_id=kwargs["organization_id"],  # type: ignore[arg-type]
                quotation_id=quote_id,
                party_id=party_id,
                source_ref=kwargs["source_ref"],  # type: ignore[arg-type]
                shipment_ref=None,
                parent_shipment_id=None,
                relation_kind=None,
                guide_code=None,
                plant_label="Gdańsk",
                carrier_label="DB Schenker",
                asn_id=UUID(asn_id),
                status="draft",
                created_by=kwargs["user_id"],  # type: ignore[arg-type]
            )

    monkeypatch.setattr("app.api.asns.QuotationService", lambda _s: _Quotes())
    monkeypatch.setattr("app.api.asns.ShipmentService", lambda _s: _Shipments())
    promoted = client.post(
        f"/api/v1/asns/{asn_id}/promote",
        headers=bearer_auth_headers(),
        json={"quotation_id": str(quote_id)},
    )
    assert promoted.status_code == 201
    body = promoted.json()
    assert body["asn_id"] == asn_id
    assert body["plant_label"] == "Gdańsk"
    assert body["quotation_id"] == str(quote_id)


def test_http_promote_unknown_asn_is_404(asn_http: object) -> None:
    client, _desk, _guides, _enf, _matches = asn_http
    response = client.post(
        f"/api/v1/asns/{uuid4()}/promote",
        headers=bearer_auth_headers(),
        json={"quotation_id": str(uuid4())},
    )
    assert response.status_code == 404
    assert "awizo" in response.json()["detail"]


def test_http_promote_respects_block_409(asn_http: object) -> None:
    client, desk, guides, enforcements, _matches = asn_http
    header = uuid4()
    desk.known_headers.add(header)
    created = client.post(
        "/api/v1/asns",
        headers=bearer_auth_headers(),
        json=_payload(header, asn_code="asn_blk", guide_code=None),
    )
    assert created.status_code == 201
    asn_id = created.json()["id"]
    guides._codes = ["lane_pl_de"]
    enforcements._kinds = ["block_409"]
    response = client.post(
        f"/api/v1/asns/{asn_id}/promote",
        headers=bearer_auth_headers(),
        json={"quotation_id": str(uuid4())},
    )
    assert response.status_code == 409
    assert "guide_code" in response.json()["detail"]

