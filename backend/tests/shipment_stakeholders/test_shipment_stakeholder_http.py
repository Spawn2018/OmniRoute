from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.shipment_stakeholder import require_stakeholder_role, require_stakeholder_source_ref
from app.main import app
from app.models.party import Party
from app.models.shipment import Shipment
from app.models.shipment_stakeholder import ShipmentStakeholder
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


class StubPartyService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: Party | None = None

    async def get_party(self, party_id: UUID) -> Party:
        if self.row is None or self.row.id != party_id:
            raise ResourceNotFound("nieznany kontrahent")
        return self.row


class StubShipmentStakeholderService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[ShipmentStakeholder] = []

    async def list_for_shipment(self, shipment_id: object) -> list[ShipmentStakeholder]:
        order_id = shipment_id if type(shipment_id) is UUID else uuid4()
        return [
            row
            for row in self.rows
            if row.shipment_id == order_id and row.superseded_by is None
        ]

    async def record_assignment(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: object,
        party_id: object,
        role: object,
        source_ref: object,
    ) -> ShipmentStakeholder:
        token = require_stakeholder_role(role)
        origin = require_stakeholder_source_ref(source_ref)
        order_id = shipment_id if type(shipment_id) is UUID else uuid4()
        counterpart = party_id if type(party_id) is UUID else uuid4()
        current = next(
            (
                row
                for row in self.rows
                if row.shipment_id == order_id
                and row.role == token
                and row.superseded_by is None
            ),
            None,
        )
        if current is not None and current.party_id == counterpart and current.source_ref == origin:
            return current
        successor = ShipmentStakeholder(
            id=uuid4(),
            organization_id=organization_id,
            shipment_id=order_id,
            party_id=counterpart,
            role=token,
            source_ref=origin,
            created_by=user_id,
        )
        if current is not None:
            current.superseded_by = successor.id
        self.rows.append(successor)
        return successor


def _shipment() -> Shipment:
    return Shipment(
        id=uuid4(),
        organization_id=uuid4(),
        quotation_id=uuid4(),
        party_id=uuid4(),
        source_ref="fixture://shipment/1",
        status="draft",
    )


def _party() -> Party:
    return Party(
        id=uuid4(),
        organization_id=uuid4(),
        legal_name="Agent",
        country_code="PL",
        roles=["agent"],
        source_ref="tenant:manual",
        is_active=True,
    )


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    ships = StubShipmentService(object())
    parties = StubPartyService(object())
    rows = StubShipmentStakeholderService(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.shipment_stakeholders.ShipmentService", lambda _s: ships)
    monkeypatch.setattr("app.api.shipment_stakeholders.PartyService", lambda _s: parties)
    monkeypatch.setattr("app.api.shipment_stakeholders.ShipmentStakeholderService", lambda _s: rows)
    ships.row = _shipment()
    parties.row = _party()
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), ships, parties, rows
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_list_and_supersede(catalog_client: object) -> None:
    client, ships, parties, _rows = catalog_client
    assert ships.row is not None
    assert parties.row is not None
    headers = bearer_auth_headers()
    first = client.post(
        "/api/v1/shipment-stakeholders",
        headers=headers,
        json={
            "shipment_id": str(ships.row.id),
            "party_id": str(parties.row.id),
            "role": "shipper",
            "source_ref": "tenant:manual",
        },
    )
    assert first.status_code == 201
    other_party = uuid4()
    parties.row = Party(
        id=other_party,
        organization_id=parties.row.organization_id,
        legal_name="Drugi",
        country_code="PL",
        roles=["agent"],
        source_ref="tenant:manual",
        is_active=True,
    )
    second = client.post(
        "/api/v1/shipment-stakeholders",
        headers=headers,
        json={
            "shipment_id": str(ships.row.id),
            "party_id": str(other_party),
            "role": "shipper",
            "source_ref": "tenant:manual",
        },
    )
    assert second.status_code == 201
    assert second.json()["id"] != first.json()["id"]
    listed = client.get(
        "/api/v1/shipment-stakeholders",
        headers=headers,
        params={"shipment_id": str(ships.row.id)},
    )
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == second.json()["id"]
    bad = client.post(
        "/api/v1/shipment-stakeholders",
        headers=headers,
        json={
            "shipment_id": str(ships.row.id),
            "party_id": str(other_party),
            "role": "sold_to",
            "source_ref": "tenant:manual",
        },
    )
    assert bad.status_code == 400
