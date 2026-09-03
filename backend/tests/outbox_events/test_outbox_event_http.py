from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.main import app
from app.models.outbox_event import OutboxEvent
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


class StubOutboxEventService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[OutboxEvent] = []

    async def list_events(self) -> list[OutboxEvent]:
        return list(self.rows)

    async def record_message_saved(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        subject_id: object,
        source_ref: str,
    ) -> OutboxEvent:
        token = UUID(str(subject_id))
        for row in self.rows:
            if row.subject_id == token:
                return row
        row = OutboxEvent(
            id=uuid4(),
            organization_id=organization_id,
            event_kind="inbound_message_saved",
            subject_id=token,
            status="pending",
            source_ref=source_ref,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    stub = StubOutboxEventService(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.outbox_events.OutboxEventService",
        lambda _session: stub,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_record_outbox_event_is_idempotent(catalog_client: TestClient) -> None:
    org_id = uuid4()
    subject = str(uuid4())
    headers = bearer_auth_headers(organization_id=org_id)
    payload = {
        "subject_id": subject,
        "source_ref": f"outbox://inbound-message/{subject}",
    }
    first = catalog_client.post("/api/v1/outbox-events", headers=headers, json=payload)
    assert first.status_code == 200
    body = first.json()
    assert body["organization_id"] == str(org_id)
    assert body["event_kind"] == "inbound_message_saved"
    assert body["status"] == "pending"
    assert body["subject_id"] == subject
    assert "amount" not in body
    second = catalog_client.post("/api/v1/outbox-events", headers=headers, json=payload)
    assert second.status_code == 200
    assert second.json()["id"] == body["id"]
    listed = catalog_client.get("/api/v1/outbox-events", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 1
