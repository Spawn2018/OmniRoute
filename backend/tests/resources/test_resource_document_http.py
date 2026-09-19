from datetime import date
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.resource_document import parse_resource_document
from app.main import app
from app.models.resource_document import ResourceDocument
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


class StubDocuments:
    def __init__(self) -> None:
        self.rows: list[ResourceDocument] = []

    async def list_documents(self) -> list[ResourceDocument]:
        return list(self.rows)

    async def record_document(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        resource_id: object,
        document_kind: object,
        valid_until: object,
        source_ref: object,
    ) -> ResourceDocument:
        fleet_id, kind, until, origin = parse_resource_document(
            resource_id,
            document_kind,
            valid_until,
            source_ref,
        )
        row = ResourceDocument(
            id=uuid4(),
            organization_id=organization_id,
            resource_id=fleet_id,
            document_kind=kind,
            valid_until=until,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def document_client(monkeypatch: pytest.MonkeyPatch) -> object:
    stub = StubDocuments()

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.resource_documents.ResourceDocumentService",
        lambda _s: stub,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), stub
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_reject_kind(document_client: object) -> None:
    client, _stub = document_client
    headers = bearer_auth_headers(organization_id=uuid4())
    fleet = uuid4()
    created = client.post(
        "/api/v1/resource-documents",
        headers=headers,
        json={
            "resource_id": str(fleet),
            "document_kind": "licence",
            "valid_until": "2027-06-01",
            "source_ref": "tenant:manual",
        },
    )
    assert created.status_code == 201
    assert created.json()["document_kind"] == "licence"
    assert created.json()["valid_until"] == "2027-06-01"
    assert created.json()["resource_id"] == str(fleet)
    listed = client.get("/api/v1/resource-documents", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == created.json()["id"]
    bad = client.post(
        "/api/v1/resource-documents",
        headers=headers,
        json={
            "resource_id": str(fleet),
            "document_kind": "ocp",
            "valid_until": "2027-06-01",
            "source_ref": "tenant:manual",
        },
    )
    assert bad.status_code == 400
    assert "dokumentu" in bad.json()["detail"]
    assert date.fromisoformat("2027-06-01")
