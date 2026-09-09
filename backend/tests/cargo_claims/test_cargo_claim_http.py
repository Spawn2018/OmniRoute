from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.cargo_claim import (
    require_claim_kind,
    require_claim_source_ref,
    require_cmr_notice_window,
    require_cmr_order,
    require_damage_code,
    require_notice_due_at,
    require_suit_due_at,
)
from app.domain.errors import ResourceNotFound
from app.main import app
from app.models.cargo_claim import CargoClaim
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


class StubShipmentService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: Shipment | None = None

    async def get_shipment(self, shipment_id: UUID) -> Shipment:
        if self.row is None or self.row.id != shipment_id:
            raise ResourceNotFound("nieznane zlecenie")
        return self.row


class StubCargoClaimService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[CargoClaim] = []

    async def list_claims(self) -> list[CargoClaim]:
        return list(self.rows)

    async def record_claim(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: UUID,
        claim_kind: str,
        damage_code: str,
        cmr_notice_window: str,
        notice_due_at: str,
        suit_due_at: str,
        source_ref: str,
    ) -> CargoClaim:
        notice = require_notice_due_at(notice_due_at)
        suit = require_suit_due_at(suit_due_at)
        require_cmr_order(notice, suit)
        row = CargoClaim(
            id=uuid4(),
            organization_id=organization_id,
            shipment_id=shipment_id,
            claim_kind=require_claim_kind(claim_kind),
            damage_code=require_damage_code(damage_code),
            cmr_notice_window=require_cmr_notice_window(cmr_notice_window),
            notice_due_at=notice,
            suit_due_at=suit,
            source_ref=require_claim_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


def _claim_json(shipment_id: UUID, **overrides: str) -> dict[str, str]:
    payload = {
        "shipment_id": str(shipment_id),
        "claim_kind": "damage",
        "damage_code": "damage",
        "cmr_notice_window": "notice_7",
        "notice_due_at": "2026-01-10",
        "suit_due_at": "2026-12-31",
        "source_ref": "fixture://cargo-claim/1",
    }
    payload.update(overrides)
    return payload


def _shipment() -> Shipment:
    return Shipment(
        id=uuid4(),
        organization_id=uuid4(),
        quotation_id=uuid4(),
        party_id=uuid4(),
        source_ref="fixture://shipment/1",
        status="draft",
    )


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    ships = StubShipmentService(object())
    claims = StubCargoClaimService(object())

    def _ships(_session: object) -> StubShipmentService:
        return ships

    def _rows(_session: object) -> StubCargoClaimService:
        return claims

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.cargo_claims.ShipmentService", _ships)
    monkeypatch.setattr("app.api.cargo_claims.CargoClaimService", _rows)
    ships.row = _shipment()
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), ships, claims
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_cargo_claim(catalog_client: object) -> None:
    client, ships, _claims = catalog_client
    assert ships.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/cargo-claims",
        headers=headers,
        json=_claim_json(ships.row.id),
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["shipment_id"] == str(ships.row.id)
    assert body["claim_kind"] == "damage"
    assert body["damage_code"] == "damage"
    assert body["cmr_notice_window"] == "notice_7"
    assert body["notice_due_at"] == "2026-01-10"
    assert body["suit_due_at"] == "2026-12-31"
    assert "amount" not in body
    listed = client.get("/api/v1/cargo-claims", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_claim_unknown_shipment_is_404(catalog_client: object) -> None:
    client, _ships, _claims = catalog_client
    response = client.post(
        "/api/v1/cargo-claims",
        headers=bearer_auth_headers(),
        json=_claim_json(uuid4()),
    )
    assert response.status_code == 404


def test_http_create_claim_unknown_kind_is_400(catalog_client: object) -> None:
    client, ships, _claims = catalog_client
    assert ships.row is not None
    response = client.post(
        "/api/v1/cargo-claims",
        headers=bearer_auth_headers(),
        json=_claim_json(ships.row.id, claim_kind="fraud"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_http_create_claim_empty_source_ref_is_400(catalog_client: object) -> None:
    client, ships, _claims = catalog_client
    assert ships.row is not None
    response = client.post(
        "/api/v1/cargo-claims",
        headers=bearer_auth_headers(),
        json=_claim_json(ships.row.id, source_ref="   "),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_http_create_claim_unknown_osd_is_400(catalog_client: object) -> None:
    client, ships, _claims = catalog_client
    assert ships.row is not None
    response = client.post(
        "/api/v1/cargo-claims",
        headers=bearer_auth_headers(),
        json=_claim_json(ships.row.id, damage_code="scratch"),
    )
    assert response.status_code == 400
    assert "osd" in response.json()["detail"]


def test_http_create_claim_unknown_window_is_400(catalog_client: object) -> None:
    client, ships, _claims = catalog_client
    assert ships.row is not None
    response = client.post(
        "/api/v1/cargo-claims",
        headers=bearer_auth_headers(),
        json=_claim_json(ships.row.id, cmr_notice_window="365"),
    )
    assert response.status_code == 400
    assert "okno" in response.json()["detail"]


def test_http_create_claim_suit_before_notice_is_400(catalog_client: object) -> None:
    client, ships, _claims = catalog_client
    assert ships.row is not None
    response = client.post(
        "/api/v1/cargo-claims",
        headers=bearer_auth_headers(),
        json=_claim_json(
            ships.row.id,
            notice_due_at="2026-12-31",
            suit_due_at="2026-01-10",
        ),
    )
    assert response.status_code == 400
    assert "kolejność" in response.json()["detail"]
