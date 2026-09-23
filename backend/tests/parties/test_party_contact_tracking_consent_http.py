from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.main import app
from app.models.party_contact import PartyContact
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
        self.organization_id = uuid4()
        self.last_kwargs: dict[str, object] = {}
        self.row = PartyContact(
            id=uuid4(),
            organization_id=self.organization_id,
            party_id=uuid4(),
            name="Anna",
            is_primary=False,
            tracking_consent=False,
        )

    async def create_contact(self, **kwargs: object) -> PartyContact:
        self.last_kwargs = kwargs
        consent = bool(kwargs.get("tracking_consent", False))
        self.row = PartyContact(
            id=uuid4(),
            organization_id=self.organization_id,
            party_id=kwargs["party_id"],  # type: ignore[arg-type]
            name=str(kwargs["name"]),
            email=None,
            phone=None,
            position=None,
            is_primary=bool(kwargs.get("is_primary", False)),
            tracking_consent=consent,
        )
        return self.row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> tuple[TestClient, StubPartyService]:
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


def test_http_create_contact_defaults_tracking_consent_false(
    catalog_client: tuple[TestClient, StubPartyService],
) -> None:
    client, stub = catalog_client
    party_id = uuid4()
    headers = bearer_auth_headers(organization_id=stub.organization_id)
    response = client.post(
        f"/api/v1/parties/{party_id}/contacts",
        headers=headers,
        json={"name": "Anna"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["tracking_consent"] is False
    assert stub.last_kwargs.get("tracking_consent") is False


def test_http_create_contact_accepts_tracking_consent_true(
    catalog_client: tuple[TestClient, StubPartyService],
) -> None:
    client, stub = catalog_client
    party_id = uuid4()
    headers = bearer_auth_headers(organization_id=stub.organization_id)
    response = client.post(
        f"/api/v1/parties/{party_id}/contacts",
        headers=headers,
        json={"name": "Bartek", "tracking_consent": True},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["tracking_consent"] is True
    assert stub.last_kwargs.get("tracking_consent") is True
