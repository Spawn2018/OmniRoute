from decimal import Decimal
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import UnknownPort
from app.main import app
from app.models.port import Port
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


class StubPortService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[Port] = []

    async def list_ports(self, search: str | None = None) -> list[Port]:
        if search is None:
            return list(self.rows)
        needle = search.strip().upper()
        return [row for row in self.rows if needle in row.unlocode or needle in row.name.upper()]

    async def create_manual_port(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        unlocode: str,
        name: str,
        country_code: str,
        lat: Decimal | None,
        lng: Decimal | None,
        is_seaport: bool,
        function_flags: list[str],
        aliases: list[str],
    ) -> Port:
        row = Port(
            id=uuid4(),
            organization_id=organization_id,
            unlocode=unlocode.replace(" ", "").upper(),
            name=name.strip(),
            country_code=country_code.upper(),
            lat=lat,
            lng=lng,
            is_seaport=is_seaport,
            function_flags=function_flags,
            aliases=aliases,
            is_official=False,
            source_ref="tenant:manual",
            created_by=user_id,
        )
        self.rows.append(row)
        return row

    async def resolve(self, raw: str) -> Port:
        token = raw.replace(" ", "").strip().upper()
        for row in self.rows:
            if row.unlocode == token or token in [alias.upper() for alias in row.aliases]:
                return row
        raise UnknownPort(f"nieznany port: {token}")


@pytest.fixture
def ports_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    stub = StubPortService(object())

    def _factory(session: object) -> StubPortService:
        return stub

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.ports.PortService", _factory)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_ports(ports_client: TestClient) -> None:
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)

    created = ports_client.post(
        "/api/v1/ports",
        headers=headers,
        json={
            "unlocode": "pl gdy",
            "name": " Gdynia ",
            "country_code": "pl",
            "lat": "54.516667",
            "lng": "18.55",
            "is_seaport": True,
            "function_flags": ["port"],
            "aliases": ["Gdingen"],
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["unlocode"] == "PLGDY"
    assert body["organization_id"] == str(org_id)
    assert body["is_official"] is False
    assert body["source_ref"] == "tenant:manual"
    assert Decimal(str(body["lat"])) == Decimal("54.516667")

    listed = ports_client.get("/api/v1/ports", headers=headers)
    assert listed.status_code == 200
    assert [row["id"] for row in listed.json()] == [body["id"]]


def test_http_list_ports_accepts_search_token(ports_client: TestClient) -> None:
    headers = bearer_auth_headers()
    ports_client.post(
        "/api/v1/ports",
        headers=headers,
        json={"unlocode": "PLGDY", "name": "Gdynia", "country_code": "PL"},
    )
    ports_client.post(
        "/api/v1/ports",
        headers=headers,
        json={"unlocode": "DEHAM", "name": "Hamburg", "country_code": "DE"},
    )

    listed = ports_client.get("/api/v1/ports", headers=headers, params={"search": "ham"})
    assert listed.status_code == 200
    assert [row["unlocode"] for row in listed.json()] == ["DEHAM"]


def test_http_resolve_returns_the_catalog_row(ports_client: TestClient) -> None:
    headers = bearer_auth_headers()
    ports_client.post(
        "/api/v1/ports",
        headers=headers,
        json={
            "unlocode": "PLGDY",
            "name": "Gdynia",
            "country_code": "PL",
            "aliases": ["Gdingen"],
        },
    )

    resolved = ports_client.get(
        "/api/v1/ports/resolve",
        headers=headers,
        params={"token": "gdingen"},
    )
    assert resolved.status_code == 200
    assert resolved.json()["unlocode"] == "PLGDY"


def test_http_resolve_rejects_loose_place_name(ports_client: TestClient) -> None:
    response = ports_client.get(
        "/api/v1/ports/resolve",
        headers=bearer_auth_headers(),
        params={"token": "gdzieś nad morzem"},
    )
    assert response.status_code == 400
    assert "nieznany port" in response.json()["detail"]
