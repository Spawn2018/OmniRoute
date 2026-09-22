from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.shipment_document import require_document_kind, require_document_source_ref
from app.main import app
from app.models.shipment import Shipment
from app.models.shipment_document import ShipmentDocument
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


class StubShipmentDocumentService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[ShipmentDocument] = []

    async def list_documents(self) -> list[ShipmentDocument]:
        return list(self.rows)

    async def record_document(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: UUID,
        document_kind: str,
        source_ref: str,
    ) -> ShipmentDocument:
        row = ShipmentDocument(
            id=uuid4(),
            organization_id=organization_id,
            shipment_id=shipment_id,
            document_kind=require_document_kind(document_kind),
            source_ref=require_document_source_ref(source_ref),
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
    documents = StubShipmentDocumentService(object())

    def _ships(_session: object) -> StubShipmentService:
        return ships

    def _docs(_session: object) -> StubShipmentDocumentService:
        return documents

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.shipment_documents.ShipmentService", _ships)
    monkeypatch.setattr("app.api.shipment_documents.ShipmentDocumentService", _docs)
    ships.row = _shipment()
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), ships, documents
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_shipment_document(catalog_client: object) -> None:
    client, ships, _documents = catalog_client
    assert ships.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/shipment-documents",
        headers=headers,
        json={
            "shipment_id": str(ships.row.id),
            "document_kind": "noted",
            "source_ref": "fixture://shipment-document/1",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["shipment_id"] == str(ships.row.id)
    assert body["document_kind"] == "noted"
    assert body["source_ref"] == "fixture://shipment-document/1"
    assert "amount" not in body
    assert "pdf" not in body
    assert "hbl" not in body

    listed = client.get("/api/v1/shipment-documents", headers=headers)
    assert listed.status_code == 200
    rows = listed.json()
    assert len(rows) == 1
    assert rows[0]["id"] == body["id"]


def test_http_create_document_unknown_shipment_is_404(catalog_client: object) -> None:
    client, _ships, _documents = catalog_client
    response = client.post(
        "/api/v1/shipment-documents",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(uuid4()),
            "document_kind": "noted",
            "source_ref": "fixture://shipment-document/1",
        },
    )
    assert response.status_code == 404


def test_http_create_document_unknown_kind_is_400(catalog_client: object) -> None:
    client, ships, _documents = catalog_client
    assert ships.row is not None
    response = client.post(
        "/api/v1/shipment-documents",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ships.row.id),
            "document_kind": "hbl",
            "source_ref": "fixture://shipment-document/1",
        },
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_http_create_document_rod_kind(catalog_client: object) -> None:
    client, ships, _documents = catalog_client
    assert ships.row is not None
    created = client.post(
        "/api/v1/shipment-documents",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ships.row.id),
            "document_kind": "rod",
            "source_ref": "fixture://shipment-document/1",
        },
    )
    assert created.status_code == 201
    assert created.json()["document_kind"] == "rod"
    assert "amount" not in created.json()


def test_http_create_document_pod_token_is_400(catalog_client: object) -> None:
    client, ships, _documents = catalog_client
    assert ships.row is not None
    response = client.post(
        "/api/v1/shipment-documents",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ships.row.id),
            "document_kind": "pod",
            "source_ref": "fixture://shipment-document/1",
        },
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_http_create_document_empty_source_ref_is_400(catalog_client: object) -> None:
    client, ships, _documents = catalog_client
    assert ships.row is not None
    response = client.post(
        "/api/v1/shipment-documents",
        headers=bearer_auth_headers(),
        json={
            "shipment_id": str(ships.row.id),
            "document_kind": "noted",
            "source_ref": "   ",
        },
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]
