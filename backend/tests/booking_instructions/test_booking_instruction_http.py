from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.booking_instruction import (
    require_booking_scope_token,
    require_instruction_source_ref,
    require_instruction_status,
    require_instruction_target_role,
)
from app.domain.errors import ResourceNotFound
from app.main import app
from app.models.booking_instruction import BookingInstruction
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


class StubBookingInstructionService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[BookingInstruction] = []

    async def list_for_shipment(self, shipment_id: object) -> list[BookingInstruction]:
        order_id = shipment_id if type(shipment_id) is UUID else uuid4()
        return [
            row
            for row in self.rows
            if row.shipment_id == order_id and row.superseded_by is None
        ]

    async def record_instruction(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: object,
        booking_scope: object,
        target_role: object,
        status: object,
        source_ref: object,
    ) -> BookingInstruction:
        scope = require_booking_scope_token(booking_scope)
        role = require_instruction_target_role(target_role)
        state = require_instruction_status(status)
        origin = require_instruction_source_ref(source_ref)
        order_id = shipment_id if type(shipment_id) is UUID else uuid4()
        current = next(
            (
                row
                for row in self.rows
                if row.shipment_id == order_id
                and row.booking_scope == scope
                and row.target_role == role
                and row.superseded_by is None
            ),
            None,
        )
        if current is not None and current.status == state and current.source_ref == origin:
            return current
        successor = BookingInstruction(
            id=uuid4(),
            organization_id=organization_id,
            shipment_id=order_id,
            booking_scope=scope,
            target_role=role,
            status=state,
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


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    ships = StubShipmentService(object())
    rows = StubBookingInstructionService(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.booking_instructions.ShipmentService", lambda _s: ships)
    monkeypatch.setattr(
        "app.api.booking_instructions.BookingInstructionService",
        lambda _s: rows,
    )
    ships.row = _shipment()
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), ships, rows
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_list_supersede_and_reject_queued(catalog_client: object) -> None:
    client, ships, _rows = catalog_client
    assert ships.row is not None
    headers = bearer_auth_headers()
    payload = {
        "shipment_id": str(ships.row.id),
        "booking_scope": "contact_exchange",
        "target_role": "origin_agent",
        "status": "suggested",
        "source_ref": "tenant:manual",
    }
    first = client.post("/api/v1/booking-instructions", headers=headers, json=payload)
    assert first.status_code == 201
    assert "amount" not in first.json()
    second = client.post(
        "/api/v1/booking-instructions",
        headers=headers,
        json={**payload, "status": "accepted"},
    )
    assert second.status_code == 201
    assert second.json()["id"] != first.json()["id"]
    listed = client.get(
        "/api/v1/booking-instructions",
        headers=headers,
        params={"shipment_id": str(ships.row.id)},
    )
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == second.json()["id"]
    bad_scope = client.post(
        "/api/v1/booking-instructions",
        headers=headers,
        json={**payload, "booking_scope": "ocean_booking"},
    )
    assert bad_scope.status_code == 400
    queued = client.post(
        "/api/v1/booking-instructions",
        headers=headers,
        json={**payload, "status": "queued"},
    )
    assert queued.status_code == 400
