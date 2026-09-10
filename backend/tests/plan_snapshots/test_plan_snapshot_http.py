from datetime import datetime
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.plan_snapshot import (
    require_author_label,
    require_recorded_at,
    require_resource_id,
    require_shipment_id,
    require_snapshot_code,
    require_snapshot_source_ref,
    require_trip_id,
)
from app.main import app
from app.models.plan_snapshot import PlanSnapshot
from tests.http_auth import bearer_auth_headers

_HITL = "2026-09-10T12:00:00+02:00"


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


class StubSnapshotDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[PlanSnapshot] = []

    async def list_rows(self) -> list[PlanSnapshot]:
        return list(self.rows)

    async def persist_snapshot(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        snapshot_code: object,
        shipment_id: object,
        trip_id: object,
        resource_id: object,
        author_label: object,
        recorded_at: object,
        source_ref: object,
    ) -> PlanSnapshot:
        row = PlanSnapshot(
            id=uuid4(),
            organization_id=organization_id,
            snapshot_code=require_snapshot_code(snapshot_code),
            shipment_id=require_shipment_id(shipment_id),
            trip_id=require_trip_id(trip_id),
            resource_id=require_resource_id(resource_id),
            author_label=require_author_label(author_label),
            recorded_at=require_recorded_at(recorded_at),
            source_ref=require_snapshot_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = StubSnapshotDesk(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.plan_snapshots.PlanSnapshotService",
        lambda _s: desk,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**overrides: object) -> dict[str, object]:
    stamp = str(uuid4())
    body: dict[str, object] = {
        "snapshot_code": "plan_v1",
        "shipment_id": stamp,
        "trip_id": stamp,
        "resource_id": stamp,
        "author_label": "Anna",
        "recorded_at": _HITL,
        "source_ref": "fixture://plan-snapshot/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_plan_snapshot(catalog_client: object) -> None:
    client, _desk = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post("/api/v1/plan-snapshots", headers=headers, json=_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["snapshot_code"] == "plan_v1"
    assert body["author_label"] == "Anna"
    assert datetime.fromisoformat(body["recorded_at"].replace("Z", "+00:00"))
    assert "buy_amount" not in body
    listed = client.get("/api/v1/plan-snapshots", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_bad_code_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/plan-snapshots",
        headers=bearer_auth_headers(),
        json=_payload(snapshot_code="X"),
    )
    assert response.status_code == 400
    assert "migawka" in response.json()["detail"]


def test_http_create_bad_shipment_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/plan-snapshots",
        headers=bearer_auth_headers(),
        json=_payload(shipment_id="nie-uuid"),
    )
    assert response.status_code == 400
    assert "zlecenie" in response.json()["detail"]


def test_http_create_bad_trip_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/plan-snapshots",
        headers=bearer_auth_headers(),
        json=_payload(trip_id="nie-uuid"),
    )
    assert response.status_code == 400
    assert "przejazd" in response.json()["detail"]


def test_http_create_bad_resource_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/plan-snapshots",
        headers=bearer_auth_headers(),
        json=_payload(resource_id="nie-uuid"),
    )
    assert response.status_code == 400
    assert "zasob" in response.json()["detail"]


def test_http_create_bad_author_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/plan-snapshots",
        headers=bearer_auth_headers(),
        json=_payload(author_label=""),
    )
    assert response.status_code == 400
    assert "autor" in response.json()["detail"]


def test_http_create_bad_time_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/plan-snapshots",
        headers=bearer_auth_headers(),
        json=_payload(recorded_at="2026-09-10T12:00:00"),
    )
    assert response.status_code == 400
    assert "czas" in response.json()["detail"]


def test_http_create_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/plan-snapshots",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://hold.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
