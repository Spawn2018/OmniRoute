from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.outbox_event import OutboxEvent


class OutboxEventRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[OutboxEvent]:
        result = await self._session.scalars(
            select(OutboxEvent).order_by(OutboxEvent.created_at.desc()),
        )
        return list(result.all())

    async def get(self, event_id: UUID) -> OutboxEvent | None:
        found = await self._session.get(OutboxEvent, event_id)
        return found if isinstance(found, OutboxEvent) else None

    async def get_by_subject(self, event_kind: str, subject_id: UUID) -> OutboxEvent | None:
        found = await self._session.scalar(
            select(OutboxEvent).where(
                OutboxEvent.event_kind == event_kind,
                OutboxEvent.subject_id == subject_id,
            ),
        )
        return found if isinstance(found, OutboxEvent) else None

    async def add(self, row: OutboxEvent) -> OutboxEvent:
        self._session.add(row)
        await self._session.flush()
        return row
