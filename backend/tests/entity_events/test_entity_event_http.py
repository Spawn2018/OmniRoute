from datetime import UTC, datetime
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.entity_event import (
    require_entity_event_kind,
    require_entity_source_ref,
    require_entity_subject_id,
    require_entity_subject_kind,
)
from app.main import app
from app.models.entity_event import EntityEvent
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


class StubEntityEventService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[EntityEvent] = []

    async def list_events(self) -> list[EntityEvent]:
        return list(self.rows)

    async def create_event(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        subject_kind: object,
        subject_id: object,
        event_kind: object,
        source_ref: str,
        occurred_at: datetime | None,
    ) -> EntityEvent:
        when = occurred_at if occurred_at is not None else datetime.now(UTC)
        row = EntityEvent(
            id=uuid4(),
            organization_id=organization_id,
            subject_kind=require_entity_subject_kind(subject_kind),
            subject_id=require_entity_subject_id(subject_id),
            event_kind=require_entity_event_kind(event_kind),
            occurred_at=when,
            source_ref=require_entity_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    stub = StubEntityEventService(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.entity_events.EntityEventService",
        lambda _session: stub,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(
    *,
    event_kind: str = "inquiry_queued",
    source_ref: str | None = None,
) -> dict[str, str]:
    subject = str(uuid4())
    return {
        "subject_kind": "carrier_inquiry",
        "subject_id": subject,
        "event_kind": event_kind,
        "source_ref": source_ref if source_ref is not None else f"entity://inquiry/{subject}",
    }


def test_http_record_entity_event_appends(catalog_client: TestClient) -> None:
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    first = catalog_client.post("/api/v1/entity-events", headers=headers, json=_payload())
    assert first.status_code == 200
    body = first.json()
    assert body["organization_id"] == str(org_id)
    assert body["event_kind"] == "inquiry_queued"
    assert body["subject_kind"] == "carrier_inquiry"
    assert "amount" not in body
    second = catalog_client.post("/api/v1/entity-events", headers=headers, json=_payload())
    assert second.status_code == 200
    assert second.json()["id"] != body["id"]
    listed = catalog_client.get("/api/v1/entity-events", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 2


def test_http_unknown_kind_is_400(catalog_client: TestClient) -> None:
    headers = bearer_auth_headers()
    response = catalog_client.post(
        "/api/v1/entity-events",
        headers=headers,
        json=_payload(event_kind="prediction_scored"),
    )
    assert response.status_code == 400
    assert "event_kind" in response.json()["detail"]


def test_http_missing_source_ref_is_400(catalog_client: TestClient) -> None:
    headers = bearer_auth_headers()
    response = catalog_client.post(
        "/api/v1/entity-events",
        headers=headers,
        json=_payload(source_ref="   "),
    )
    assert response.status_code == 400
