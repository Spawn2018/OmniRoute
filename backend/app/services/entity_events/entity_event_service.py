from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entity_event import (
    require_entity_event_kind,
    require_entity_source_ref,
    require_entity_subject_id,
    require_entity_subject_kind,
)
from app.models.entity_event import EntityEvent
from app.repositories.entity_events.entity_event_repository import EntityEventRepository


class EntityEventService:
    def __init__(self, session: AsyncSession) -> None:
        self._events = EntityEventRepository(session)

    async def list_events(self) -> list[EntityEvent]:
        return await self._events.list_all()

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
        return await self._events.add(row)
