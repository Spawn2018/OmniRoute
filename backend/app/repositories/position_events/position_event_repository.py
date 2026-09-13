from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.position_event import PositionEvent


class PositionEventRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_events(self) -> list[PositionEvent]:
        packed = await self._session.scalars(
            select(PositionEvent).order_by(PositionEvent.event_code, PositionEvent.id),
        )
        return list(packed.all())

    async def add_event(self, row: PositionEvent) -> PositionEvent:
        self._session.add(row)
        await self._session.flush()
        return row
