from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import NetworkConflict, ResourceNotFound, UnknownNetwork
from app.main import app
from app.models.network import Network
from app.models.network_member import NetworkMember
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
        self.row: Party | None = None

    async def get_party(self, party_id: UUID) -> Party:
        if self.row is None or self.row.id != party_id:
            raise ResourceNotFound("nieznany kontrahent")
        return self.row


def _party() -> Party:
    return Party(
        id=uuid4(),
        organization_id=uuid4(),
        legal_name="Agent",
        country_code="PL",
        roles=["agent"],
        source_ref="tenant:manual",
        is_active=True,
    )


class StubNetworkService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[Network] = []
        self.members: list[NetworkMember] = []
        self.party_country: dict[UUID, str] = {}

    async def list_networks(self) -> list[Network]:
        return list(self.rows)

    async def create_network(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        code: str,
        name: str,
        aliases: list[str],
        website: str | None,
        region_scope: str | None,
        is_global: bool,
    ) -> Network:
        row = Network(
            id=uuid4(),
            organization_id=organization_id,
            code=code.strip().lower(),
            name=name.strip(),
            aliases=[alias.strip() for alias in aliases],
            website=website,
            region_scope=region_scope,
            is_global=is_global,
            source_ref="tenant:manual",
            created_by=user_id,
        )
        self.rows.append(row)
        return row

    async def resolve(self, raw: str) -> Network:
        token = raw.strip().lower()
        for row in self.rows:
            if row.code == token or token in row.aliases:
                return row
        raise UnknownNetwork(f"nieznana sieć: {token}")

    async def get_network(self, network_id: UUID) -> Network:
        for row in self.rows:
            if row.id == network_id:
                return row
        raise UnknownNetwork(f"nieznana sieć: {network_id}")

    async def list_members(
        self,
        network_id: UUID,
        *,
        country_code: str | None = None,
    ) -> list[NetworkMember]:
        await self.get_network(network_id)
        rows = [row for row in self.members if row.network_id == network_id]
        if country_code is None:
            return rows
        # Stub HTTP: country z mapy party — brak party_id = poza filtrem
        return [
            row
            for row in rows
            if row.party_id is not None and self.party_country.get(row.party_id) == country_code
        ]

    async def create_member(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        network_id: UUID,
        member_code: str,
        legal_name: str,
        party_id: UUID,
    ) -> NetworkMember:
        await self.get_network(network_id)
        token = member_code.strip().lower()
        for row in self.members:
            if row.network_id == network_id and row.member_code == token:
                raise NetworkConflict(f"członek {token} już istnieje w sieci")
        row = NetworkMember(
            id=uuid4(),
            organization_id=organization_id,
            network_id=network_id,
            member_code=token,
            legal_name=legal_name.strip(),
            party_id=party_id,
            source_ref="tenant:manual",
            created_by=user_id,
        )
        self.members.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    stub = StubNetworkService(object())
    parties = StubPartyService(object())
    parties.row = _party()
    stub.party_country[parties.row.id] = parties.row.country_code

    def _factory(session: object) -> StubNetworkService:
        return stub

    def _parties(_session: object) -> StubPartyService:
        return parties

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.networks.NetworkService", _factory)
    monkeypatch.setattr("app.api.networks.PartyService", _parties)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), parties
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_networks(catalog_client: object) -> None:
    catalog_client, _parties = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = catalog_client.post(
        "/api/v1/networks",
        headers=headers,
        json={
            "code": "wca",
            "name": "WCA",
            "aliases": ["wca_ww"],
            "website": "https://wca.com",
            "is_global": True,
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["code"] == "wca"
    assert body["organization_id"] == str(org_id)
    assert body["aliases"] == ["wca_ww"]
    assert body["is_global"] is True
    assert body["source_ref"] == "tenant:manual"
    assert "amount" not in body

    listed = catalog_client.get("/api/v1/networks", headers=headers)
    assert listed.status_code == 200
    rows = listed.json()
    assert len(rows) == 1
    assert rows[0]["id"] == body["id"]


def test_http_resolve_unknown_token_is_rejected(catalog_client: object) -> None:
    catalog_client, _parties = catalog_client
    response = catalog_client.get(
        "/api/v1/networks/resolve",
        headers=bearer_auth_headers(),
        params={"token": "xyz"},
    )
    assert response.status_code == 400
    assert "nieznana sieć" in response.json()["detail"]


def test_http_create_rejects_client_source_ref(catalog_client: object) -> None:
    catalog_client, _parties = catalog_client
    response = catalog_client.post(
        "/api/v1/networks",
        headers=bearer_auth_headers(),
        json={
            "code": "wca",
            "name": "WCA",
            "aliases": [],
            "source_ref": "forged:origin",
        },
    )
    assert response.status_code == 422


def test_http_resolve_returns_catalog_row(catalog_client: object) -> None:
    catalog_client, _parties = catalog_client
    headers = bearer_auth_headers()
    catalog_client.post(
        "/api/v1/networks",
        headers=headers,
        json={"code": "wca", "name": "WCA", "aliases": ["wca_ww"], "is_global": True},
    )
    resolved = catalog_client.get(
        "/api/v1/networks/resolve",
        headers=headers,
        params={"token": "wca_ww"},
    )
    assert resolved.status_code == 200
    assert resolved.json()["code"] == "wca"


def test_http_create_and_list_network_members(catalog_client: object) -> None:
    catalog_client, parties = catalog_client
    assert parties.row is not None
    headers = bearer_auth_headers()
    created = catalog_client.post(
        "/api/v1/networks",
        headers=headers,
        json={"code": "wca", "name": "WCA", "aliases": [], "is_global": True},
    )
    network_id = created.json()["id"]
    member = catalog_client.post(
        f"/api/v1/networks/{network_id}/members",
        headers=headers,
        json={
            "member_code": "Agent_A",
            "legal_name": "Agent Alpha",
            "party_id": str(parties.row.id),
        },
    )
    assert member.status_code == 201
    assert member.json()["member_code"] == "agent_a"
    assert member.json()["legal_name"] == "Agent Alpha"
    assert member.json()["network_id"] == network_id
    assert member.json()["party_id"] == str(parties.row.id)
    listed = catalog_client.get(f"/api/v1/networks/{network_id}/members", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == member.json()["id"]
    again = catalog_client.post(
        f"/api/v1/networks/{network_id}/members",
        headers=headers,
        json={
            "member_code": "agent_a",
            "legal_name": "Agent Alpha",
            "party_id": str(parties.row.id),
        },
    )
    assert again.status_code == 400


def test_http_member_without_party_id_is_rejected(catalog_client: object) -> None:
    catalog_client, _parties = catalog_client
    headers = bearer_auth_headers()
    created = catalog_client.post(
        "/api/v1/networks",
        headers=headers,
        json={"code": "wca", "name": "WCA", "aliases": [], "is_global": True},
    )
    response = catalog_client.post(
        f"/api/v1/networks/{created.json()['id']}/members",
        headers=headers,
        json={"member_code": "agent_a", "legal_name": "Agent Alpha"},
    )
    assert response.status_code == 422


def test_http_member_unknown_party_is_404(catalog_client: object) -> None:
    catalog_client, _parties = catalog_client
    headers = bearer_auth_headers()
    created = catalog_client.post(
        "/api/v1/networks",
        headers=headers,
        json={"code": "wca", "name": "WCA", "aliases": [], "is_global": True},
    )
    response = catalog_client.post(
        f"/api/v1/networks/{created.json()['id']}/members",
        headers=headers,
        json={
            "member_code": "agent_a",
            "legal_name": "Agent Alpha",
            "party_id": str(uuid4()),
        },
    )
    assert response.status_code == 404


def test_http_members_unknown_network_is_rejected(catalog_client: object) -> None:
    catalog_client, _parties = catalog_client
    response = catalog_client.get(
        f"/api/v1/networks/{uuid4()}/members",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 400
    assert "nieznana sieć" in response.json()["detail"]


def test_http_members_filter_by_country_code(catalog_client: object) -> None:
    catalog_client, parties = catalog_client
    assert parties.row is not None
    headers = bearer_auth_headers()
    created = catalog_client.post(
        "/api/v1/networks",
        headers=headers,
        json={"code": "wca", "name": "WCA", "aliases": [], "is_global": True},
    )
    network_id = created.json()["id"]
    member = catalog_client.post(
        f"/api/v1/networks/{network_id}/members",
        headers=headers,
        json={
            "member_code": "agent_nl",
            "legal_name": "Rotterdam Agent",
            "party_id": str(parties.row.id),
        },
    )
    assert member.status_code == 201

    all_rows = catalog_client.get(f"/api/v1/networks/{network_id}/members", headers=headers)
    assert all_rows.status_code == 200
    assert len(all_rows.json()) == 1

    empty_filter = catalog_client.get(
        f"/api/v1/networks/{network_id}/members",
        headers=headers,
        params={"country_code": "  "},
    )
    assert empty_filter.status_code == 200
    assert len(empty_filter.json()) == 1

    match = catalog_client.get(
        f"/api/v1/networks/{network_id}/members",
        headers=headers,
        params={"country_code": "pl"},
    )
    assert match.status_code == 200
    assert len(match.json()) == 1
    assert match.json()[0]["id"] == member.json()["id"]

    miss = catalog_client.get(
        f"/api/v1/networks/{network_id}/members",
        headers=headers,
        params={"country_code": "NL"},
    )
    assert miss.status_code == 200
    assert miss.json() == []

    bad_short = catalog_client.get(
        f"/api/v1/networks/{network_id}/members",
        headers=headers,
        params={"country_code": "N"},
    )
    assert bad_short.status_code == 400
    assert "country_code" in bad_short.json()["detail"]

    bad_digits = catalog_client.get(
        f"/api/v1/networks/{network_id}/members",
        headers=headers,
        params={"country_code": "12"},
    )
    assert bad_digits.status_code == 400
    assert "ISO" in bad_digits.json()["detail"]
