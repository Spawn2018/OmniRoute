from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.fuel_index import (
    require_index_kind,
    require_index_source_ref,
    require_index_value,
    require_published_on,
)
from app.main import app
from app.models.fuel_index import FuelIndex
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


class StubFuelIndexService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[FuelIndex] = []

    async def list_indexes(self) -> list[FuelIndex]:
        return list(self.rows)

    async def record_index(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        index_kind: str,
        published_on: str,
        index_value: str,
        source_ref: str,
    ) -> FuelIndex:
        row = FuelIndex(
            id=uuid4(),
            organization_id=organization_id,
            index_kind=require_index_kind(index_kind),
            published_on=require_published_on(published_on),
            index_value=require_index_value(index_value),
            source_ref=require_index_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    rows = StubFuelIndexService(object())

    def _rows(_session: object) -> StubFuelIndexService:
        return rows

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.fuel_indexes.FuelIndexService", _rows)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), rows
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "index_kind": "fsc",
        "published_on": "2026-03-01",
        "index_value": "1.2500",
        "source_ref": "fixture://fuel-index/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_fuel_index(catalog_client: object) -> None:
    client, _rows = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post("/api/v1/fuel-indexes", headers=headers, json=_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["index_kind"] == "fsc"
    assert body["index_value"] == "1.2500"
    assert "buy_amount" not in body
    listed = client.get("/api/v1/fuel-indexes", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_index_bad_kind_is_400(catalog_client: object) -> None:
    client, _rows = catalog_client
    response = client.post(
        "/api/v1/fuel-indexes",
        headers=bearer_auth_headers(),
        json=_payload(index_kind="oil"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_http_create_index_zero_value_is_400(catalog_client: object) -> None:
    client, _rows = catalog_client
    response = client.post(
        "/api/v1/fuel-indexes",
        headers=bearer_auth_headers(),
        json=_payload(index_value="0"),
    )
    assert response.status_code == 400
    assert "indeks" in response.json()["detail"]


def test_http_create_index_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _rows = catalog_client
    response = client.post(
        "/api/v1/fuel-indexes",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://hold.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
