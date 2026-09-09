from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.twin_mark import TwinMark


class TwinMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._db = session

    async def fetch_marks(self) -> list[TwinMark]:
        stmt = select(TwinMark).order_by(TwinMark.source_ref, TwinMark.id)
        executed = await self._db.execute(stmt)
        return list(executed.scalars())

    async def add(self, row: TwinMark) -> TwinMark:
        self._db.add(row)
        await self._db.flush()
        return row
