from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import ResourceNotFound
from app.domain.kreptd_licence import (
    require_kreptd_source_ref,
    require_licence_no,
    require_party_id,
)
from app.main import app
from app.models.kreptd_licence import KreptdLicence
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


class StubPartyLookup:
    def __init__(self, session: object) -> None:
        self._session = session
        self.row: Party | None = None

    async def get_party(self, party_id: UUID) -> Party:
        if self.row is None or self.row.id != party_id:
            raise ResourceNotFound("nieznany kontrahent")
        return self.row


class StubKreptdDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[KreptdLicence] = []

    async def list_licences(self) -> list[KreptdLicence]:
        return list(self.rows)

    async def persist_licence(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        party_id: object,
        licence_no: object,
        source_ref: object,
    ) -> KreptdLicence:
        row = KreptdLicence(
            id=uuid4(),
            organization_id=organization_id,
            party_id=require_party_id(party_id),
            licence_no=require_licence_no(licence_no),
            source_ref=require_kreptd_source_ref(source_ref),
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
    licences = StubKreptdDesk(object())
    parties = StubPartyLookup(object())
    parties.row = _party()

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.kreptd_licences.KreptdLicenceService",
        lambda _s: licences,
    )
    monkeypatch.setattr("app.api.kreptd_licences.PartyService", lambda _s: parties)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), licences, parties
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(party_id: UUID, **overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "party_id": str(party_id),
        "licence_no": "GITD-12345678",
        "source_ref": "fixture://kreptd-licence/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_kreptd_licence(catalog_client: object) -> None:
    client, _licences, parties = catalog_client
    assert parties.row is not None
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/kreptd-licences",
        headers=headers,
        json=_payload(parties.row.id),
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["licence_no"] == "GITD-12345678"
    assert "buy_amount" not in body
    listed = client.get("/api/v1/kreptd-licences", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_bad_licence_no_is_400(catalog_client: object) -> None:
    client, _licences, parties = catalog_client
    assert parties.row is not None
    response = client.post(
        "/api/v1/kreptd-licences",
        headers=bearer_auth_headers(),
        json=_payload(parties.row.id, licence_no="http://kreptd.gitd.gov.pl/x"),
    )
    assert response.status_code == 400
    assert "licencja" in response.json()["detail"]


def test_http_create_kreptd_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _licences, parties = catalog_client
    assert parties.row is not None
    response = client.post(
        "/api/v1/kreptd-licences",
        headers=bearer_auth_headers(),
        json=_payload(parties.row.id, source_ref="http://hold.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
