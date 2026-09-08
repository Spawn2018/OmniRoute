from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import InvalidPartyData, PartyConflict
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
        self.existing_id = uuid4()
        self.row = Party(
            id=uuid4(),
            organization_id=uuid4(),
            legal_name="ACME",
            country_code="DE",
            roles=["vendor"],
            eori="DE1234567",
            source_ref="tenant:manual",
            is_active=True,
        )

    async def create_party(self, **kwargs: object) -> Party:
        eori = kwargs.get("eori")
        tax_id = kwargs.get("tax_id")
        vat_eu = kwargs.get("vat_eu")
        duns = kwargs.get("duns")
        if tax_id is None and eori is None and vat_eu is None and duns is None:
            raise InvalidPartyData("wymagany identyfikator biznesowy")
        if eori == "DE1234567":
            raise PartyConflict(
                "kontrahent z tym eori już istnieje",
                existing_party_id=self.existing_id,
            )
        return self.row


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


def test_http_create_party_without_business_id_is_400(
    catalog_client: tuple[TestClient, StubPartyService],
) -> None:
    client, stub = catalog_client
    headers = bearer_auth_headers(organization_id=stub.row.organization_id)
    response = client.post(
        "/api/v1/parties",
        headers=headers,
        json={
            "legal_name": "ACME",
            "country_code": "DE",
            "roles": ["vendor"],
        },
    )
    assert response.status_code == 400
    assert "identyfikator biznesowy" in response.json()["detail"]


def test_http_duplicate_eori_is_409_with_href(
    catalog_client: tuple[TestClient, StubPartyService],
) -> None:
    client, stub = catalog_client
    headers = bearer_auth_headers(organization_id=stub.row.organization_id)
    response = client.post(
        "/api/v1/parties",
        headers=headers,
        json={
            "legal_name": "ACME",
            "country_code": "DE",
            "roles": ["vendor"],
            "eori": "DE1234567",
        },
    )
    assert response.status_code == 409
    body = response.json()
    assert body["existing_party_id"] == str(stub.existing_id)
    assert body["href"] == f"/parties/{stub.existing_id}"
    assert "eori" in body["detail"]
