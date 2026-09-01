from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import UnknownCommodityCode
from app.main import app
from app.models.commodity_code import CommodityCode
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


class StubCommodityCodeService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[CommodityCode] = []

    async def list_codes(self) -> list[CommodityCode]:
        return list(self.rows)

    async def create_code(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        code: str,
        name: str,
        aliases: list[str],
    ) -> CommodityCode:
        row = CommodityCode(
            id=uuid4(),
            organization_id=organization_id,
            code=code.strip(),
            name=name.strip(),
            aliases=[alias.strip() for alias in aliases],
            source_ref="tenant:manual",
            created_by=user_id,
        )
        self.rows.append(row)
        return row

    async def resolve(self, raw: str) -> CommodityCode:
        token = raw.strip()
        for row in self.rows:
            if row.code == token or token in row.aliases:
                return row
        raise UnknownCommodityCode(f"nieznany kod towarowy: {token}")


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    stub = StubCommodityCodeService(object())

    def _factory(session: object) -> StubCommodityCodeService:
        return stub

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.commodity_codes.CommodityCodeService", _factory)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_commodity_codes(catalog_client: TestClient) -> None:
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = catalog_client.post(
        "/api/v1/commodity-codes",
        headers=headers,
        json={"code": "0805", "name": "Citrus", "aliases": ["080510"]},
    )
    assert created.status_code == 201
    body = created.json()
    assert body["code"] == "0805"
    assert body["organization_id"] == str(org_id)
    assert body["aliases"] == ["080510"]
    assert body["source_ref"] == "tenant:manual"
    assert "amount" not in body

    listed = catalog_client.get("/api/v1/commodity-codes", headers=headers)
    assert listed.status_code == 200
    rows = listed.json()
    assert len(rows) == 1
    assert rows[0]["id"] == body["id"]


def test_http_resolve_unknown_token_is_rejected(catalog_client: TestClient) -> None:
    response = catalog_client.get(
        "/api/v1/commodity-codes/resolve",
        headers=bearer_auth_headers(),
        params={"token": "9999"},
    )
    assert response.status_code == 400
    assert "nieznany kod towarowy" in response.json()["detail"]


def test_http_create_rejects_client_source_ref(catalog_client: TestClient) -> None:
    response = catalog_client.post(
        "/api/v1/commodity-codes",
        headers=bearer_auth_headers(),
        json={
            "code": "0805",
            "name": "Citrus",
            "aliases": [],
            "source_ref": "forged:origin",
        },
    )
    assert response.status_code == 422


def test_http_resolve_returns_catalog_row(catalog_client: TestClient) -> None:
    headers = bearer_auth_headers()
    catalog_client.post(
        "/api/v1/commodity-codes",
        headers=headers,
        json={"code": "0805", "name": "Citrus", "aliases": ["080510"]},
    )
    resolved = catalog_client.get(
        "/api/v1/commodity-codes/resolve",
        headers=headers,
        params={"token": "080510"},
    )
    assert resolved.status_code == 200
    assert resolved.json()["code"] == "0805"
