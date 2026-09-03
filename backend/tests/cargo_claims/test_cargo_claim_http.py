from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.cargo_claim import require_claim_kind, require_claim_source_ref
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
        source_ref: str,
    ) -> CargoClaim:
        row = CargoClaim(
            id=uuid4(),
            organization_id=organization_id,
            shipment_id=shipment_id,
            claim_kind=require_claim_kind(claim_kind),
            source_ref=require_claim_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


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
        json={
            "shipment_id": str(ships.row.id),
            "claim_kind": "damage",
            "source_ref": "fixture://cargo-claim/1",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["shipment_id"] == str(ships.row.id)
    assert body["claim_kind"] == "damage"
    assert "amount" not in body
    listed = client.get("/api/v1/cargo-claims", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_claim_unknown_shipment_is_404(catalog_client: object) -> None:
    client, _ships, _claims = catalog_client
    response = client.post(
        "/api/v1/cargo-claims",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(uuid4()),
            "claim_kind": "damage",
            "source_ref": "fixture://cargo-claim/1",
        },
    )
    assert response.status_code == 404


def test_http_create_claim_unknown_kind_is_400(catalog_client: object) -> None:
    client, ships, _claims = catalog_client
    assert ships.row is not None
    response = client.post(
        "/api/v1/cargo-claims",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ships.row.id),
            "claim_kind": "fraud",
            "source_ref": "fixture://cargo-claim/1",
        },
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_http_create_claim_empty_source_ref_is_400(catalog_client: object) -> None:
    client, ships, _claims = catalog_client
    assert ships.row is not None
    response = client.post(
        "/api/v1/cargo-claims",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ships.row.id),
            "claim_kind": "damage",
            "source_ref": "   ",
        },
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]
