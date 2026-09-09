from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.war_room_mark import require_incident_kind, require_room_source_ref
from app.main import app
from app.models.war_room_mark import WarRoomMark
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


class StubWarRooms:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[WarRoomMark] = []

    async def list_incidents(self) -> list[WarRoomMark]:
        return list(self.rows)

    async def record_incident(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        incident_kind: object,
        source_ref: object,
    ) -> WarRoomMark:
        row = WarRoomMark(
            id=uuid4(),
            organization_id=organization_id,
            incident_kind=require_incident_kind(incident_kind),
            source_ref=require_room_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    rooms = StubWarRooms(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.war_room_marks.WarRoomMarkService", lambda _s: rooms)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), rooms
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "incident_kind": "weather",
        "source_ref": "fixture://war-room-mark/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_war_room_mark(catalog_client: object) -> None:
    client, _rooms = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post("/api/v1/war-room-marks", headers=headers, json=_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["incident_kind"] == "weather"
    assert "buy_amount" not in body
    listed = client.get("/api/v1/war-room-marks", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_bad_kind_is_400(catalog_client: object) -> None:
    client, _rooms = catalog_client
    response = client.post(
        "/api/v1/war-room-marks",
        headers=bearer_auth_headers(),
        json=_payload(incident_kind="chat"),
    )
    assert response.status_code == 400
    assert "incydent" in response.json()["detail"]


def test_http_create_war_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _rooms = catalog_client
    response = client.post(
        "/api/v1/war-room-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://war.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
