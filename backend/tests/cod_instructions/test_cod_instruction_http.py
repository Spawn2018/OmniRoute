from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.cod_instruction import (
    require_collection_status,
    require_instruction_code,
    require_instruction_source_ref,
)
from app.domain.errors import ResourceNotFound
from app.main import app
from app.models.cod_instruction import CodInstruction
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


class StubCodInstructionService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[CodInstruction] = []

    async def list_instructions(self) -> list[CodInstruction]:
        return list(self.rows)

    async def record_instruction(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: UUID,
        instruction_code: str,
        collection_status: str,
        source_ref: str,
    ) -> CodInstruction:
        row = CodInstruction(
            id=uuid4(),
            organization_id=organization_id,
            shipment_id=shipment_id,
            instruction_code=require_instruction_code(instruction_code),
            collection_status=require_collection_status(collection_status),
            source_ref=require_instruction_source_ref(source_ref),
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
    rows = StubCodInstructionService(object())

    def _ships(_session: object) -> StubShipmentService:
        return ships

    def _rows(_session: object) -> StubCodInstructionService:
        return rows

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.cod_instructions.ShipmentService", _ships)
    monkeypatch.setattr("app.api.cod_instructions.CodInstructionService", _rows)
    ships.row = _shipment()
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), ships, rows
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_cod_instruction(catalog_client: object) -> None:
    client, ships, _rows = catalog_client
    assert ships.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/cod-instructions",
        headers=headers,
        json={
            "shipment_id": str(ships.row.id),
            "instruction_code": "cod_west",
            "collection_status": "noted",
            "source_ref": "fixture://cod-instruction/1",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["shipment_id"] == str(ships.row.id)
    assert body["instruction_code"] == "cod_west"
    assert body["collection_status"] == "noted"
    assert "amount" not in body
    assert "buy_amount" not in body
    listed = client.get("/api/v1/cod-instructions", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_cod_unknown_shipment_is_404(catalog_client: object) -> None:
    client, _ships, _rows = catalog_client
    response = client.post(
        "/api/v1/cod-instructions",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(uuid4()),
            "instruction_code": "cod_west",
            "collection_status": "noted",
            "source_ref": "fixture://cod-instruction/1",
        },
    )
    assert response.status_code == 404


def test_http_create_cod_unknown_status_is_400(catalog_client: object) -> None:
    client, ships, _rows = catalog_client
    assert ships.row is not None
    response = client.post(
        "/api/v1/cod-instructions",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ships.row.id),
            "instruction_code": "cod_west",
            "collection_status": "settled",
            "source_ref": "fixture://cod-instruction/1",
        },
    )
    assert response.status_code == 400
    assert "status" in response.json()["detail"]


def test_http_create_cod_empty_code_is_400(catalog_client: object) -> None:
    client, ships, _rows = catalog_client
    assert ships.row is not None
    response = client.post(
        "/api/v1/cod-instructions",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ships.row.id),
            "instruction_code": "   ",
            "collection_status": "noted",
            "source_ref": "fixture://cod-instruction/1",
        },
    )
    assert response.status_code == 400
    assert "snake" in response.json()["detail"]


def test_http_create_cod_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, ships, _rows = catalog_client
    assert ships.row is not None
    response = client.post(
        "/api/v1/cod-instructions",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ships.row.id),
            "instruction_code": "cod_west",
            "collection_status": "noted",
            "source_ref": "http://hold.example/x",
        },
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
