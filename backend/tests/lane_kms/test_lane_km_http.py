from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.lane_km import (
    require_km_code,
    require_lane_km,
    require_lane_source_ref,
)
from app.main import app
from app.models.lane_km import LaneKm
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


class StubLaneKmDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[LaneKm] = []

    async def list_rows(self) -> list[LaneKm]:
        return list(self.rows)

    async def persist_lane_km(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        km_code: object,
        loaded_km: object,
        empty_km: object,
        approach_km: object,
        source_ref: object,
    ) -> LaneKm:
        row = LaneKm(
            id=uuid4(),
            organization_id=organization_id,
            km_code=require_km_code(km_code),
            loaded_km=require_lane_km(loaded_km, "ladowny"),
            empty_km=require_lane_km(empty_km, "pusty"),
            approach_km=require_lane_km(approach_km, "dolot"),
            source_ref=require_lane_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = StubLaneKmDesk(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.lane_kms.LaneKmService",
        lambda _s: desk,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "km_code": "backhaul_a",
        "loaded_km": "120.5",
        "empty_km": "40",
        "approach_km": "15.25",
        "source_ref": "fixture://lane-km/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_lane_km(catalog_client: object) -> None:
    client, _desk = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post("/api/v1/lane-kms", headers=headers, json=_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["km_code"] == "backhaul_a"
    assert body["loaded_km"] == "120.5000"
    assert body["empty_km"] == "40.0000"
    assert body["approach_km"] == "15.2500"
    assert "buy_amount" not in body
    assert "margin" not in body
    listed = client.get("/api/v1/lane-kms", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_zero_km_is_legal(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/lane-kms",
        headers=bearer_auth_headers(),
        json=_payload(empty_km="0"),
    )
    assert response.status_code == 201
    assert response.json()["empty_km"] == "0.0000"


def test_http_create_bad_code_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/lane-kms",
        headers=bearer_auth_headers(),
        json=_payload(km_code="X"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_http_create_float_loaded_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/lane-kms",
        headers=bearer_auth_headers(),
        json=_payload(loaded_km=1.5),
    )
    assert response.status_code == 400
    assert "ladowny" in response.json()["detail"]


def test_http_create_bool_empty_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/lane-kms",
        headers=bearer_auth_headers(),
        json=_payload(empty_km=True),
    )
    assert response.status_code == 400
    assert "pusty" in response.json()["detail"]


def test_http_create_negative_approach_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/lane-kms",
        headers=bearer_auth_headers(),
        json=_payload(approach_km="-1"),
    )
    assert response.status_code == 400
    assert "dolot" in response.json()["detail"]


def test_http_create_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/lane-kms",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://hold.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
