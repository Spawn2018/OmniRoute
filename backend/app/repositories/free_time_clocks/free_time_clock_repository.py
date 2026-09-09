from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.free_time_clock import FreeTimeClock


class FreeTimeClockRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_marks(self) -> list[FreeTimeClock]:
        packed = await self._session.scalars(
            select(FreeTimeClock).order_by(FreeTimeClock.created_at.desc(), FreeTimeClock.id),
        )
        return list(packed.all())

    async def add(self, row: FreeTimeClock) -> FreeTimeClock:
        self._session.add(row)
        await self._session.flush()
        return row
