from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import UnknownNetwork
from app.main import app
from app.models.network import Network
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


class StubNetworkService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[Network] = []

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


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    stub = StubNetworkService(object())

    def _factory(session: object) -> StubNetworkService:
        return stub

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.networks.NetworkService", _factory)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_networks(catalog_client: TestClient) -> None:
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


def test_http_resolve_unknown_token_is_rejected(catalog_client: TestClient) -> None:
    response = catalog_client.get(
        "/api/v1/networks/resolve",
        headers=bearer_auth_headers(),
        params={"token": "xyz"},
    )
    assert response.status_code == 400
    assert "nieznana sieć" in response.json()["detail"]


def test_http_create_rejects_client_source_ref(catalog_client: TestClient) -> None:
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


def test_http_resolve_returns_catalog_row(catalog_client: TestClient) -> None:
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
