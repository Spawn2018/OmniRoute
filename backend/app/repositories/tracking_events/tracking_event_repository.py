from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tracking_event import TrackingEvent


class TrackingEventRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[TrackingEvent]:
        result = await self._session.scalars(
            select(TrackingEvent).order_by(TrackingEvent.occurred_at.desc()),
        )
        return list(result.all())

    async def add(self, row: TrackingEvent) -> TrackingEvent:
        self._session.add(row)
        await self._session.flush()
        return row
