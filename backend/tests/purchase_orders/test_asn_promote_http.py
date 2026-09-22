from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound, ShipmentConflict
from app.main import app
from app.models.asn import Asn
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


def _sample_asn() -> Asn:
    return Asn(
        id=uuid4(),
        organization_id=uuid4(),
        purchase_order_id=uuid4(),
        asn_code="asn_01",
        plant_label="pl-de",
        carrier_label=None,
        ship_ref_label=None,
        guide_code="lane_pl_de",
        source_ref="fixture://asn/1",
        created_by=uuid4(),
    )


def _sample_quote(organization_id: UUID) -> Quotation:
    return Quotation(
        id=uuid4(),
        organization_id=organization_id,
        charge_code="THC",
        rate_line_id=uuid4(),
        amount=Decimal("10.0000"),
        currency="EUR",
        source_ref="tariff://a",
        party_id=uuid4(),
    )


def _bind_promote(
    monkeypatch: pytest.MonkeyPatch,
    *,
    asn: Asn,
    quote: Quotation,
    shipments: list[Shipment],
) -> None:
    class _AsnDesk:
        async def get_notice(self, asn_id: UUID) -> Asn:
            if asn_id != asn.id:
                raise ResourceNotFound("nieznane awizo")
            return asn

    class _QuoteDesk:
        async def get_quotation(self, quotation_id: UUID) -> Quotation:
            if quotation_id != quote.id:
                raise ResourceNotFound("nieznana wycena")
            return quote

    class _ShipDesk:
        async def create_shipment(self, **kwargs: object) -> Shipment:
            hitl = kwargs.get("hitl")
            asn_id = getattr(hitl, "asn_id", None) if hitl is not None else None
            if any(row.asn_id == asn_id for row in shipments):
                raise ShipmentConflict("to awizo już ma zlecenie")
            row = Shipment(
                id=uuid4(),
                organization_id=kwargs["organization_id"],  # type: ignore[arg-type]
                quotation_id=kwargs["quotation_id"],  # type: ignore[arg-type]
                party_id=kwargs["party_id"],  # type: ignore[arg-type]
                source_ref=kwargs["source_ref"],  # type: ignore[arg-type]
                shipment_ref=None,
                parent_shipment_id=None,
                relation_kind=None,
                guide_code=getattr(hitl, "guide_code", None),  # type: ignore[arg-type]
                plant_label=getattr(hitl, "plant_label", None),  # type: ignore[arg-type]
                carrier_label=getattr(hitl, "carrier_label", None),  # type: ignore[arg-type]
                asn_id=asn_id,  # type: ignore[arg-type]
                is_waste=False,
                status="draft",
                created_by=kwargs["user_id"],  # type: ignore[arg-type]
            )
            shipments.append(row)
            return row

    class _GuideDesk:
        async def list_guides(self) -> list[object]:
            return [
                type(
                    "G",
                    (),
                    {
                        "guide_code": "lane_pl_de",
                        "lane_label": "pl-de",
                        "mode_label": None,
                    },
                )()
            ]

    class _EmptyMarks:
        async def list_marks(self) -> list[object]:
            return []

    monkeypatch.setattr("app.api.asns.AsnService", lambda _s: _AsnDesk())
    monkeypatch.setattr("app.api.asns.QuotationService", lambda _s: _QuoteDesk())
    monkeypatch.setattr("app.api.asns.ShipmentService", lambda _s: _ShipDesk())
    monkeypatch.setattr("app.api.asns.RoutingGuideService", lambda _s: _GuideDesk())
    monkeypatch.setattr(
        "app.api.asns.RoutingGuideEnforcementService",
        lambda _s: _EmptyMarks(),
    )
    monkeypatch.setattr(
        "app.api.asns.RoutingGuideMatchService",
        lambda _s: _EmptyMarks(),
    )


@pytest.fixture
def promote_http(monkeypatch: pytest.MonkeyPatch) -> object:
    asn = _sample_asn()
    quote = _sample_quote(asn.organization_id)
    shipments: list[Shipment] = []
    _bind_promote(monkeypatch, asn=asn, quote=quote, shipments=shipments)

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), asn, quote, shipments
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_promote_asn_creates_shipment(promote_http: object) -> None:
    client, asn, quote, shipments = promote_http
    created = client.post(
        f"/api/v1/asns/{asn.id}/promote",
        headers=bearer_auth_headers(),
        json={"quotation_id": str(quote.id), "source_ref": "fixture://shipment/p1"},
    )
    assert created.status_code == 201
    body = created.json()
    assert body["guide_code"] == "lane_pl_de"
    assert body["plant_label"] == "pl-de"
    assert body["asn_id"] == str(asn.id)
    assert len(shipments) == 1


def test_http_promote_unknown_asn_is_404(promote_http: object) -> None:
    client, _asn, quote, _ships = promote_http
    response = client.post(
        f"/api/v1/asns/{uuid4()}/promote",
        headers=bearer_auth_headers(),
        json={"quotation_id": str(quote.id)},
    )
    assert response.status_code == 404


def test_http_promote_duplicate_asn_conflicts(promote_http: object) -> None:
    client, asn, quote, _ships = promote_http
    payload = {
        "quotation_id": str(quote.id),
        "source_ref": "fixture://shipment/p1",
    }
    first = client.post(
        f"/api/v1/asns/{asn.id}/promote",
        headers=bearer_auth_headers(),
        json=payload,
    )
    assert first.status_code == 201
    second = client.post(
        f"/api/v1/asns/{asn.id}/promote",
        headers=bearer_auth_headers(),
        json={**payload, "source_ref": "fixture://shipment/p2"},
    )
    assert second.status_code == 400
    assert "awizo" in second.json()["detail"]
