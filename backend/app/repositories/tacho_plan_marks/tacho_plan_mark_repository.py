from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tacho_plan_mark import TachoPlanMark


class TachoPlanMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[TachoPlanMark]:
        packed = await self._session.scalars(
            select(TachoPlanMark).order_by(
                TachoPlanMark.mark_code,
                TachoPlanMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: TachoPlanMark) -> TachoPlanMark:
        self._session.add(row)
        await self._session.flush()
        return row
