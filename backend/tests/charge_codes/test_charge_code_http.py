from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import UnknownChargeCode
from app.main import app
from app.models.charge_code import ChargeCode
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


class StubChargeCodeService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[ChargeCode] = []

    async def list_codes(self) -> list[ChargeCode]:
        return list(self.rows)

    async def create_code(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        code: str,
        name: str,
        aliases: list[str],
        source_ref: str,
    ) -> ChargeCode:
        origin = source_ref.strip()
        if origin == "":
            from app.domain.errors import InvalidSourceRef

            raise InvalidSourceRef("source_ref jest obowiązkowy")
        row = ChargeCode(
            id=uuid4(),
            organization_id=organization_id,
            code=code.strip().upper(),
            name=name.strip(),
            aliases=[alias.strip().upper() for alias in aliases],
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row

    async def resolve(self, raw: str) -> ChargeCode:
        token = raw.strip().upper()
        for row in self.rows:
            if row.code == token or token in row.aliases:
                return row
        raise UnknownChargeCode(f"nieznany kod opłaty: {token}")


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    stub = StubChargeCodeService(object())

    def _factory(session: object) -> StubChargeCodeService:
        return stub

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.charge_codes.ChargeCodeService", _factory)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_charge_codes(catalog_client: TestClient) -> None:
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = catalog_client.post(
        "/api/v1/charge-codes",
        headers=headers,
        json={
            "code": "BAF",
            "name": "Bunker",
            "aliases": ["BUNKER"],
            "source_ref": "tenant:manual",
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["code"] == "BAF"
    assert body["organization_id"] == str(org_id)
    assert body["aliases"] == ["BUNKER"]
    assert body["source_ref"] == "tenant:manual"
    assert "rate_line" not in body
    assert "buy" not in body
    assert "sell" not in body

    listed = catalog_client.get("/api/v1/charge-codes", headers=headers)
    assert listed.status_code == 200
    rows = listed.json()
    assert len(rows) == 1
    assert rows[0]["id"] == body["id"]


def test_http_resolve_unknown_token_is_rejected(catalog_client: TestClient) -> None:
    response = catalog_client.get(
        "/api/v1/charge-codes/resolve",
        headers=bearer_auth_headers(),
        params={"token": "LOOSE"},
    )
    assert response.status_code == 400
    assert "nieznany kod opłaty" in response.json()["detail"]


def test_http_resolve_returns_catalog_row(catalog_client: TestClient) -> None:
    headers = bearer_auth_headers()
    catalog_client.post(
        "/api/v1/charge-codes",
        headers=headers,
        json={
            "code": "THC",
            "name": "Terminal",
            "aliases": ["TERMINAL"],
            "source_ref": "tenant:manual",
        },
    )
    resolved = catalog_client.get(
        "/api/v1/charge-codes/resolve",
        headers=headers,
        params={"token": "terminal"},
    )
    assert resolved.status_code == 200
    assert resolved.json()["code"] == "THC"


def test_http_rejects_blank_source_ref(catalog_client: TestClient) -> None:
    response = catalog_client.post(
        "/api/v1/charge-codes",
        headers=bearer_auth_headers(),
        json={"code": "WAITING", "name": "Waiting", "aliases": [], "source_ref": "   "},
    )
    assert response.status_code == 400
    assert "source_ref" in response.json()["detail"]


def test_http_allows_exp1_waiting_token(catalog_client: TestClient) -> None:
    created = catalog_client.post(
        "/api/v1/charge-codes",
        headers=bearer_auth_headers(),
        json={
            "code": "WAITING",
            "name": "Waiting time",
            "aliases": [],
            "source_ref": "fixture://charge-code/waiting",
        },
    )
    assert created.status_code == 201
    assert created.json()["code"] == "WAITING"
