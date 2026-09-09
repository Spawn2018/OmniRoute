from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.party_document import (
    require_document_kind,
    require_party_document_source_ref,
    require_party_id,
)
from app.main import app
from app.models.party import Party
from app.models.party_document import PartyDocument
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


class StubPartyLookup:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: Party | None = None

    async def get_party(self, party_id: UUID) -> Party:
        if self.row is None or self.row.id != party_id:
            raise ResourceNotFound("nieznany kontrahent")
        return self.row


class StubPartyDocDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[PartyDocument] = []

    async def list_documents(self) -> list[PartyDocument]:
        return list(self.rows)

    async def persist_document(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        party_id: object,
        document_kind: object,
        source_ref: object,
    ) -> PartyDocument:
        row = PartyDocument(
            id=uuid4(),
            organization_id=organization_id,
            party_id=require_party_id(party_id),
            document_kind=require_document_kind(document_kind),
            source_ref=require_party_document_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


def _party() -> Party:
    return Party(
        id=uuid4(),
        organization_id=uuid4(),
        legal_name="Haulier",
        country_code="PL",
        roles=["carrier"],
        source_ref="fixture://party/1",
        is_active=True,
        created_by=uuid4(),
    )


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    documents = StubPartyDocDesk(object())
    parties = StubPartyLookup(object())
    parties.row = _party()

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.party_documents.PartyDocumentService",
        lambda _s: documents,
    )
    monkeypatch.setattr("app.api.party_documents.PartyService", lambda _s: parties)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), documents, parties
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(party_id: UUID, **overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "party_id": str(party_id),
        "document_kind": "ocp",
        "source_ref": "fixture://party-document/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_party_document(catalog_client: object) -> None:
    client, _documents, parties = catalog_client
    assert parties.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/party-documents",
        headers=headers,
        json=_payload(parties.row.id),
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["document_kind"] == "ocp"
    assert "buy_amount" not in body
    listed = client.get("/api/v1/party-documents", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_bad_document_kind_is_400(catalog_client: object) -> None:
    client, _documents, parties = catalog_client
    assert parties.row is not None
    response = client.post(
        "/api/v1/party-documents",
        headers=bearer_auth_headers(),
        json=_payload(parties.row.id, document_kind="X"),
    )
    assert response.status_code == 400
    assert "dokument" in response.json()["detail"]


def test_http_create_party_document_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _documents, parties = catalog_client
    assert parties.row is not None
    response = client.post(
        "/api/v1/party-documents",
        headers=bearer_auth_headers(),
        json=_payload(parties.row.id, source_ref="http://hold.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
