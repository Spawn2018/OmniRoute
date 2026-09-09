from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.free_time_clock import (
    require_clock_kind,
    require_clock_source_ref,
    require_free_days,
)
from app.main import app
from app.models.free_time_clock import FreeTimeClock
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


class StubClockDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[FreeTimeClock] = []

    async def list_marks(self) -> list[FreeTimeClock]:
        return list(self.rows)

    async def persist_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        clock_kind: object,
        free_days: object,
        source_ref: object,
    ) -> FreeTimeClock:
        row = FreeTimeClock(
            id=uuid4(),
            organization_id=organization_id,
            clock_kind=require_clock_kind(clock_kind),
            free_days=require_free_days(free_days),
            source_ref=require_clock_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    marks = StubClockDesk(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.free_time_clocks.FreeTimeClockService", lambda _s: marks)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), marks
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "clock_kind": "detention",
        "free_days": 7,
        "source_ref": "fixture://free-time-clock/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_free_time_clock(catalog_client: object) -> None:
    client, _marks = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post("/api/v1/free-time-clocks", headers=headers, json=_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["clock_kind"] == "detention"
    assert body["free_days"] == 7
    assert "buy_amount" not in body
    assert "remaining" not in body
    listed = client.get("/api/v1/free-time-clocks", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_bad_kind_is_400(catalog_client: object) -> None:
    client, _marks = catalog_client
    response = client.post(
        "/api/v1/free-time-clocks",
        headers=bearer_auth_headers(),
        json=_payload(clock_kind="eta"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_http_create_negative_days_is_400(catalog_client: object) -> None:
    client, _marks = catalog_client
    response = client.post(
        "/api/v1/free-time-clocks",
        headers=bearer_auth_headers(),
        json=_payload(free_days=-1),
    )
    assert response.status_code == 400
    assert "dni" in response.json()["detail"]


def test_http_create_clock_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _marks = catalog_client
    response = client.post(
        "/api/v1/free-time-clocks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://hold.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
