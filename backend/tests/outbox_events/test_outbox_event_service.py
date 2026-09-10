from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.models.outbox_event import OutboxEvent
from app.services.outbox_events.outbox_event_service import OutboxEventService


class MemoryEvents:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[OutboxEvent] = []

    async def get_by_subject(self, event_kind: str, subject_id: object) -> OutboxEvent | None:
        for row in self.rows:
            if row.event_kind == event_kind and row.subject_id == subject_id:
                return row
        return None

    async def add(self, row: OutboxEvent) -> OutboxEvent:
        self.rows.append(row)
        return row


@pytest.fixture
def outbox_service(monkeypatch: pytest.MonkeyPatch) -> OutboxEventService:
    monkeypatch.setattr(
        "app.services.outbox_events.outbox_event_service.OutboxEventRepository",
        MemoryEvents,
    )
    return OutboxEventService(AsyncMock())


@pytest.mark.asyncio
async def test_record_template_saved_is_idempotent(
    outbox_service: OutboxEventService,
) -> None:
    org = uuid4()
    user = uuid4()
    subject = uuid4()
    origin = f"outbox://task-template/{subject}"
    first = await outbox_service.record_template_saved(
        organization_id=org,
        user_id=user,
        subject_id=subject,
        source_ref=origin,
    )
    second = await outbox_service.record_template_saved(
        organization_id=org,
        user_id=user,
        subject_id=subject,
        source_ref=origin,
    )
    assert first.id == second.id
    assert first.event_kind == "task_template_saved"


@pytest.mark.asyncio
async def test_two_kinds_share_subject_as_two_rows(
    outbox_service: OutboxEventService,
) -> None:
    org = uuid4()
    user = uuid4()
    subject = uuid4()
    template = await outbox_service.record_template_saved(
        organization_id=org,
        user_id=user,
        subject_id=subject,
        source_ref=f"outbox://task-template/{subject}",
    )
    inbound = await outbox_service.record_message_saved(
        organization_id=org,
        user_id=user,
        subject_id=subject,
        source_ref=f"outbox://inbound-message/{subject}",
    )
    assert inbound.id != template.id
    assert inbound.event_kind == "inbound_message_saved"
    assert template.event_kind == "task_template_saved"
