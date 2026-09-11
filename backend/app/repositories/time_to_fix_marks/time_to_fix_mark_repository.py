from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.time_to_fix_mark import TimeToFixMark


class TimeToFixMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[TimeToFixMark]:
        packed = await self._session.scalars(
            select(TimeToFixMark).order_by(
                TimeToFixMark.mark_code,
                TimeToFixMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: TimeToFixMark) -> TimeToFixMark:
        self._session.add(row)
        await self._session.flush()
        return row
