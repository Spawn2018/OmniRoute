from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schedule_exception_mark import ScheduleExceptionMark


class ScheduleExceptionMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[ScheduleExceptionMark]:
        packed = await self._session.scalars(
            select(ScheduleExceptionMark).order_by(
                ScheduleExceptionMark.mark_code,
                ScheduleExceptionMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: ScheduleExceptionMark) -> ScheduleExceptionMark:
        self._session.add(row)
        await self._session.flush()
        return row
