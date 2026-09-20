from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.stop_group import (
    require_stop_group_code,
    require_stop_group_shipment_id,
    require_stop_group_source_ref,
)
from app.main import app
from app.models.shipment import Shipment
from app.models.stop_group import StopGroup
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


class StubStopGroupService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[StopGroup] = []

    async def list_groups(self) -> list[StopGroup]:
        return list(self.rows)

    async def record_group(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: object,
        group_code: object,
        source_ref: object,
    ) -> StopGroup:
        row = StopGroup(
            id=uuid4(),
            organization_id=organization_id,
            shipment_id=require_stop_group_shipment_id(shipment_id),
            group_code=require_stop_group_code(group_code),
            source_ref=require_stop_group_source_ref(source_ref),
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
    rows = StubStopGroupService(object())

    def _ships(_session: object) -> StubShipmentService:
        return ships

    def _rows(_session: object) -> StubStopGroupService:
        return rows

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.stop_groups.ShipmentService", _ships)
    monkeypatch.setattr("app.api.stop_groups.StopGroupService", _rows)
    ships.row = _shipment()
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), ships, rows
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_stop_group(catalog_client: object) -> None:
    client, ships, _rows = catalog_client
    assert ships.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/stop-groups",
        headers=headers,
        json={
            "shipment_id": str(ships.row.id),
            "group_code": "GRP1",
            "source_ref": "fixture://stop-group/1",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["shipment_id"] == str(ships.row.id)
    assert body["group_code"] == "GRP1"
    assert "amount" not in body
    listed = client.get("/api/v1/stop-groups", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_rejects_missing_shipment(catalog_client: object) -> None:
    client, _ships, _rows = catalog_client
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/stop-groups",
        headers=headers,
        json={
            "group_code": "GRP1",
            "source_ref": "fixture://stop-group/1",
        },
    )
    assert reply.status_code == 400
    assert "zlecenie" in reply.json()["detail"]


def test_http_create_rejects_unknown_shipment(catalog_client: object) -> None:
    client, ships, _rows = catalog_client
    ships.row = _shipment()
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/stop-groups",
        headers=headers,
        json={
            "shipment_id": str(uuid4()),
            "group_code": "GRP1",
            "source_ref": "fixture://stop-group/1",
        },
    )
    assert reply.status_code == 404


def test_http_create_rejects_bad_group_code(catalog_client: object) -> None:
    client, ships, _rows = catalog_client
    assert ships.row is not None
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/stop-groups",
        headers=headers,
        json={
            "shipment_id": str(ships.row.id),
            "group_code": "x",
            "source_ref": "fixture://stop-group/1",
        },
    )
    assert reply.status_code == 400
    assert "grupa" in reply.json()["detail"]


def test_http_create_rejects_foreign_source(catalog_client: object) -> None:
    client, ships, _rows = catalog_client
    assert ships.row is not None
    headers = bearer_auth_headers()
    reply = client.post(
        "/api/v1/stop-groups",
        headers=headers,
        json={
            "shipment_id": str(ships.row.id),
            "group_code": "GRP1",
            "source_ref": "http://evil.example/x",
        },
    )
    assert reply.status_code == 400
    assert "obce" in reply.json()["detail"]
