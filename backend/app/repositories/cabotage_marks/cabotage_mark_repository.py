from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cabotage_mark import CabotageMark


class CabotageMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[CabotageMark]:
        packed = await self._session.scalars(
            select(CabotageMark).order_by(
                CabotageMark.mark_code,
                CabotageMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: CabotageMark) -> CabotageMark:
        self._session.add(row)
        await self._session.flush()
        return row
