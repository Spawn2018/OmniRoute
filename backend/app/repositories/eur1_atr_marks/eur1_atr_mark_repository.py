from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.eur1_atr_mark import Eur1AtrMark


class Eur1AtrMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[Eur1AtrMark]:
        packed = await self._session.scalars(
            select(Eur1AtrMark).order_by(
                Eur1AtrMark.mark_code,
                Eur1AtrMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: Eur1AtrMark) -> Eur1AtrMark:
        self._session.add(row)
        await self._session.flush()
        return row
