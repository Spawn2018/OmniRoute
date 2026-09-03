from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.outbox_event import (
    inbound_message_saved_kind,
    outbox_pending_status,
    require_outbox_source_ref,
    require_outbox_subject_id,
)
from app.models.outbox_event import OutboxEvent
from app.repositories.outbox_events.outbox_event_repository import OutboxEventRepository


class OutboxEventService:
    def __init__(self, session: AsyncSession) -> None:
        self._events = OutboxEventRepository(session)

    async def list_events(self) -> list[OutboxEvent]:
        return await self._events.list_all()

    async def record_message_saved(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        subject_id: object,
        source_ref: str,
    ) -> OutboxEvent:
        kind = inbound_message_saved_kind()
        token = require_outbox_subject_id(subject_id)
        found = await self._events.get_by_subject(kind, token)
        if found is not None:
            return found
        row = OutboxEvent(
            id=uuid4(),
            organization_id=organization_id,
            event_kind=kind,
            subject_id=token,
            status=outbox_pending_status(),
            source_ref=require_outbox_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._events.add(row)
