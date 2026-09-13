from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.circle_sim import (
    require_circle_pair,
    require_circle_source_ref,
    require_sim_code,
)
from app.main import app
from app.models.circle_sim import CircleSim
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


class StubCircleDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[CircleSim] = []

    async def list_rows(self) -> list[CircleSim]:
        return list(self.rows)

    async def list_pairs(self) -> list[object]:
        return []

    async def persist_circle_sim(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        sim_code: object,
        unload_unlocode: object,
        load_unlocode: object,
        source_ref: object,
    ) -> CircleSim:
        unload, load = require_circle_pair(unload_unlocode, load_unlocode)
        row = CircleSim(
            id=uuid4(),
            organization_id=organization_id,
            sim_code=require_sim_code(sim_code),
            unload_unlocode=unload,
            load_unlocode=load,
            source_ref=require_circle_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = StubCircleDesk(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.circle_sims.CircleSimService",
        lambda _s: desk,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "sim_code": "backhaul_a",
        "unload_unlocode": "PLGDY",
        "load_unlocode": "DEHAM",
        "source_ref": "fixture://circle-sim/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_circle_sim(catalog_client: object) -> None:
    client, _desk = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post("/api/v1/circle-sims", headers=headers, json=_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["sim_code"] == "backhaul_a"
    assert body["unload_unlocode"] == "PLGDY"
    assert body["load_unlocode"] == "DEHAM"
    assert "buy_amount" not in body
    assert "loaded_km" not in body
    listed = client.get("/api/v1/circle-sims", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_get_pairs_is_200(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.get("/api/v1/circle-sim-pairs", headers=bearer_auth_headers())
    assert response.status_code == 200
    assert response.json() == []


def test_post_pairs_is_405(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/circle-sim-pairs",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 405
    assert "odczytem" in response.json()["detail"]


def test_http_create_bad_code_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/circle-sims",
        headers=bearer_auth_headers(),
        json=_payload(sim_code="X"),
    )
    assert response.status_code == 400
    assert "kolko" in response.json()["detail"]


def test_http_create_bad_unload_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/circle-sims",
        headers=bearer_auth_headers(),
        json=_payload(unload_unlocode="xx"),
    )
    assert response.status_code == 400
    assert "rozladunek" in response.json()["detail"]


def test_http_create_bad_load_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/circle-sims",
        headers=bearer_auth_headers(),
        json=_payload(load_unlocode="yy"),
    )
    assert response.status_code == 400
    assert "zaladunek" in response.json()["detail"]


def test_http_create_same_ends_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/circle-sims",
        headers=bearer_auth_headers(),
        json=_payload(load_unlocode="PLGDY"),
    )
    assert response.status_code == 400
    assert "para" in response.json()["detail"]


def test_http_create_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/circle-sims",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://hold.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
