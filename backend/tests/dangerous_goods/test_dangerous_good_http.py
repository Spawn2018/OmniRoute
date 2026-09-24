from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.dangerous_good import (
    normalize_adr_tunnel_code,
    normalize_imdg_class,
    normalize_packing_group,
    normalize_segregation_group,
    require_limited_quantity,
    require_marine_pollutant,
)
from app.domain.errors import UnknownDangerousGood
from app.main import app
from app.models.dangerous_good import DangerousGood
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


class StubDangerousGoodService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[DangerousGood] = []

    async def list_goods(self) -> list[DangerousGood]:
        return list(self.rows)

    async def create_good(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        un_number: str,
        imdg_class: str,
        name: str,
        aliases: list[str],
        adr_tunnel_code: str,
        segregation_group: str,
        packing_group: str,
        marine_pollutant: bool,
        limited_quantity: bool,
    ) -> DangerousGood:
        row = DangerousGood(
            id=uuid4(),
            organization_id=organization_id,
            un_number=un_number.strip(),
            imdg_class=normalize_imdg_class(imdg_class),
            adr_tunnel_code=normalize_adr_tunnel_code(adr_tunnel_code),
            segregation_group=normalize_segregation_group(segregation_group),
            packing_group=normalize_packing_group(packing_group),
            marine_pollutant=require_marine_pollutant(marine_pollutant),
            limited_quantity=require_limited_quantity(limited_quantity),
            name=name.strip(),
            aliases=[alias.strip() for alias in aliases],
            source_ref="tenant:manual",
            created_by=user_id,
        )
        self.rows.append(row)
        return row

    async def resolve(self, raw: str) -> DangerousGood:
        token = raw.strip()
        if token.upper().startswith("UN"):
            token = token[2:].strip()
        for row in self.rows:
            if row.un_number == token or token in row.aliases:
                return row
        raise UnknownDangerousGood(f"nieznany numer UN: {token}")


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    stub = StubDangerousGoodService(object())

    def _factory(session: object) -> StubDangerousGoodService:
        return stub

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.dangerous_goods.DangerousGoodService", _factory)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_create_and_list_dangerous_goods(catalog_client: TestClient) -> None:
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = catalog_client.post(
        "/api/v1/dangerous-goods",
        headers=headers,
        json={
            "un_number": "1203",
            "imdg_class": "3",
            "name": "Petrol",
            "aliases": ["1213"],
            "adr_tunnel_code": "D",
            "segregation_group": "sg1",
            "packing_group": "II",
            "marine_pollutant": False,
            "limited_quantity": False,
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["un_number"] == "1203"
    assert body["imdg_class"] == "3"
    assert body["adr_tunnel_code"] == "D"
    assert body["segregation_group"] == "sg1"
    assert body["packing_group"] == "II"
    assert body["marine_pollutant"] is False
    assert body["limited_quantity"] is False
    assert body["organization_id"] == str(org_id)
    assert body["aliases"] == ["1213"]
    assert body["source_ref"] == "tenant:manual"
    assert "amount" not in body

    listed = catalog_client.get("/api/v1/dangerous-goods", headers=headers)
    assert listed.status_code == 200
    rows = listed.json()
    assert len(rows) == 1
    assert rows[0]["id"] == body["id"]


def test_http_resolve_unknown_token_is_rejected(catalog_client: TestClient) -> None:
    response = catalog_client.get(
        "/api/v1/dangerous-goods/resolve",
        headers=bearer_auth_headers(),
        params={"token": "9999"},
    )
    assert response.status_code == 400
    assert "nieznany numer UN" in response.json()["detail"]


def test_http_create_rejects_client_source_ref(catalog_client: TestClient) -> None:
    response = catalog_client.post(
        "/api/v1/dangerous-goods",
        headers=bearer_auth_headers(),
        json={
            "un_number": "1203",
            "imdg_class": "3",
            "name": "Petrol",
            "aliases": [],
            "adr_tunnel_code": "D",
            "segregation_group": "none",
            "packing_group": "II",
            "marine_pollutant": False,
            "limited_quantity": False,
            "source_ref": "forged:origin",
        },
    )
    assert response.status_code == 422


def test_http_resolve_returns_catalog_row(catalog_client: TestClient) -> None:
    headers = bearer_auth_headers()
    catalog_client.post(
        "/api/v1/dangerous-goods",
        headers=headers,
        json={
            "un_number": "1203",
            "imdg_class": "3",
            "name": "Petrol",
            "aliases": ["1213"],
            "adr_tunnel_code": "D",
            "segregation_group": "sg1",
            "packing_group": "II",
            "marine_pollutant": False,
            "limited_quantity": False,
        },
    )
    resolved = catalog_client.get(
        "/api/v1/dangerous-goods/resolve",
        headers=headers,
        params={"token": "1213"},
    )
    assert resolved.status_code == 200
    assert resolved.json()["un_number"] == "1203"


def test_http_create_unknown_tunnel_is_400(catalog_client: TestClient) -> None:
    response = catalog_client.post(
        "/api/v1/dangerous-goods",
        headers=bearer_auth_headers(),
        json={
            "un_number": "1203",
            "imdg_class": "3",
            "name": "Petrol",
            "aliases": [],
            "adr_tunnel_code": "F",
            "segregation_group": "none",
            "packing_group": "II",
            "marine_pollutant": False,
            "limited_quantity": False,
        },
    )
    assert response.status_code == 400
    assert "tunel" in response.json()["detail"]


def test_http_create_unknown_segregation_is_400(catalog_client: TestClient) -> None:
    response = catalog_client.post(
        "/api/v1/dangerous-goods",
        headers=bearer_auth_headers(),
        json={
            "un_number": "1203",
            "imdg_class": "3",
            "name": "Petrol",
            "aliases": [],
            "adr_tunnel_code": "D",
            "segregation_group": "sg99",
            "packing_group": "II",
            "marine_pollutant": False,
            "limited_quantity": False,
        },
    )
    assert response.status_code == 400
    assert "segregacja" in response.json()["detail"]

def test_http_create_unknown_packing_is_400(catalog_client: TestClient) -> None:
    response = catalog_client.post(
        "/api/v1/dangerous-goods",
        headers=bearer_auth_headers(),
        json={
            "un_number": "1203",
            "imdg_class": "3",
            "name": "Petrol",
            "aliases": [],
            "adr_tunnel_code": "D",
            "segregation_group": "none",
            "packing_group": "IV",
            "marine_pollutant": False,
            "limited_quantity": False,
        },
    )
    assert response.status_code == 400
    assert "pakowanie" in response.json()["detail"]


def test_http_create_marine_pollutant_true(catalog_client: TestClient) -> None:
    response = catalog_client.post(
        "/api/v1/dangerous-goods",
        headers=bearer_auth_headers(),
        json={
            "un_number": "3082",
            "imdg_class": "9",
            "name": "Environmentally hazardous",
            "aliases": [],
            "adr_tunnel_code": "E",
            "segregation_group": "none",
            "packing_group": "III",
            "marine_pollutant": True,
            "limited_quantity": False,
        },
    )
    assert response.status_code == 201
    assert response.json()["marine_pollutant"] is True


def test_http_create_limited_quantity_true(catalog_client: TestClient) -> None:
    response = catalog_client.post(
        "/api/v1/dangerous-goods",
        headers=bearer_auth_headers(),
        json={
            "un_number": "1170",
            "imdg_class": "3",
            "name": "Ethanol LQ",
            "aliases": [],
            "adr_tunnel_code": "D",
            "segregation_group": "none",
            "packing_group": "II",
            "marine_pollutant": False,
            "limited_quantity": True,
        },
    )
    assert response.status_code == 201
    assert response.json()["limited_quantity"] is True

