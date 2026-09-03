from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.operational_exception import require_exception_kind, require_exception_source_ref
from app.main import app
from app.models.operational_exception import OperationalException
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


class StubOperationalExceptionService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[OperationalException] = []

    async def list_exceptions(self) -> list[OperationalException]:
        return list(self.rows)

    async def record_exception(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: UUID,
        exception_kind: str,
        source_ref: str,
    ) -> OperationalException:
        row = OperationalException(
            id=uuid4(),
            organization_id=organization_id,
            shipment_id=shipment_id,
            exception_kind=require_exception_kind(exception_kind),
            source_ref=require_exception_source_ref(source_ref),
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
    exceptions = StubOperationalExceptionService(object())

    def _ships(_session: object) -> StubShipmentService:
        return ships

    def _exc(_session: object) -> StubOperationalExceptionService:
        return exceptions

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.operational_exceptions.ShipmentService", _ships)
    monkeypatch.setattr("app.api.operational_exceptions.OperationalExceptionService", _exc)
    ships.row = _shipment()
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), ships, exceptions
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_operational_exception(catalog_client: object) -> None:
    client, ships, _exceptions = catalog_client
    assert ships.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/operational-exceptions",
        headers=headers,
        json={
            "shipment_id": str(ships.row.id),
            "exception_kind": "noted",
            "source_ref": "fixture://operational-exception/1",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["shipment_id"] == str(ships.row.id)
    assert body["exception_kind"] == "noted"
    assert body["source_ref"] == "fixture://operational-exception/1"
    assert "amount" not in body
    assert "eta" not in body
    assert "ais" not in body

    listed = client.get("/api/v1/operational-exceptions", headers=headers)
    assert listed.status_code == 200
    rows = listed.json()
    assert len(rows) == 1
    assert rows[0]["id"] == body["id"]


def test_http_create_exception_unknown_shipment_is_404(catalog_client: object) -> None:
    client, _ships, _exceptions = catalog_client
    response = client.post(
        "/api/v1/operational-exceptions",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(uuid4()),
            "exception_kind": "noted",
            "source_ref": "fixture://operational-exception/1",
        },
    )
    assert response.status_code == 404


def test_http_create_exception_unknown_kind_is_400(catalog_client: object) -> None:
    client, ships, _exceptions = catalog_client
    assert ships.row is not None
    response = client.post(
        "/api/v1/operational-exceptions",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ships.row.id),
            "exception_kind": "hold",
            "source_ref": "fixture://operational-exception/1",
        },
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_http_create_exception_empty_source_ref_is_400(catalog_client: object) -> None:
    client, ships, _exceptions = catalog_client
    assert ships.row is not None
    response = client.post(
        "/api/v1/operational-exceptions",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ships.row.id),
            "exception_kind": "noted",
            "source_ref": "   ",
        },
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]
