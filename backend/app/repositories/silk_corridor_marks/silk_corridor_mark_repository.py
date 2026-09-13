from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.silk_corridor_mark import SilkCorridorMark


class SilkCorridorMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[SilkCorridorMark]:
        packed = await self._session.scalars(
            select(SilkCorridorMark).order_by(
                SilkCorridorMark.mark_code,
                SilkCorridorMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: SilkCorridorMark) -> SilkCorridorMark:
        self._session.add(row)
        await self._session.flush()
        return row
