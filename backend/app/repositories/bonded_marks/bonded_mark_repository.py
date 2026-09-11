from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.bonded_mark import BondedMark


class BondedMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[BondedMark]:
        packed = await self._session.scalars(
            select(BondedMark).order_by(BondedMark.mark_code, BondedMark.id),
        )
        return list(packed.all())

    async def add_mark(self, row: BondedMark) -> BondedMark:
        self._session.add(row)
        await self._session.flush()
        return row
