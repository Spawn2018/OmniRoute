from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.main import app
from app.models.party import Party
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


class StubPartyService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row = Party(
            id=uuid4(),
            organization_id=uuid4(),
            legal_name="ACME",
            country_code="PL",
            roles=["customer"],
            source_ref="tenant:manual",
            is_active=True,
        )

    async def get_party(self, party_id: UUID) -> Party:
        if party_id != self.row.id:
            raise ResourceNotFound(f"nieznany kontrahent: {party_id}")
        return self.row

    async def screen_sanctions(self, party_id: UUID, sanctions_list_ref: object) -> Party:
        from app.domain.party import normalize_sanctions_list_ref

        row = await self.get_party(party_id)
        row.sanctions_list_ref = normalize_sanctions_list_ref(sanctions_list_ref)
        row.sanctions_checked_at = datetime.now(UTC)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    stub = StubPartyService(object())

    def _factory(session: object) -> StubPartyService:
        return stub

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.parties.PartyService", _factory)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), stub
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_screen_sanctions_keeps_source_ref_and_has_no_score(
    catalog_client: tuple[TestClient, StubPartyService],
) -> None:
    client, stub = catalog_client
    headers = bearer_auth_headers(organization_id=stub.row.organization_id)
    response = client.post(
        f"/api/v1/parties/{stub.row.id}/screen-sanctions",
        headers=headers,
        json={"sanctions_list_ref": "fixture://sanctions/eu-1"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["sanctions_list_ref"] == "fixture://sanctions/eu-1"
    assert body["sanctions_checked_at"] is not None
    assert body["source_ref"] == "tenant:manual"
    assert "risk_score" not in body
    assert "score" not in body
    assert body["credit_limit"] is None


def test_http_screen_sanctions_empty_ref_is_rejected(
    catalog_client: tuple[TestClient, StubPartyService],
) -> None:
    client, stub = catalog_client
    response = client.post(
        f"/api/v1/parties/{stub.row.id}/screen-sanctions",
        headers=bearer_auth_headers(),
        json={"sanctions_list_ref": "   "},
    )
    assert response.status_code == 400
    assert "wskazanie listy" in response.json()["detail"]


def test_http_screen_sanctions_live_http_ref_is_rejected(
    catalog_client: tuple[TestClient, StubPartyService],
) -> None:
    client, stub = catalog_client
    response = client.post(
        f"/api/v1/parties/{stub.row.id}/screen-sanctions",
        headers=bearer_auth_headers(),
        json={"sanctions_list_ref": "https://example.test/list"},
    )
    assert response.status_code == 400
    assert "fixture://sanctions/" in response.json()["detail"]
