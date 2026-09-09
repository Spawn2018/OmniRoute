from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.rank_mark import RankMark


class RankMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._db = session

    async def fetch_axes(self) -> list[RankMark]:
        stmt = select(RankMark).order_by(RankMark.rank_kind, RankMark.id)
        executed = await self._db.execute(stmt)
        return list(executed.scalars())

    async def add(self, row: RankMark) -> RankMark:
        self._db.add(row)
        await self._db.flush()
        return row
