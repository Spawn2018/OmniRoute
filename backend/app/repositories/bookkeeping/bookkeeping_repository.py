from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.bookkeeping import Bookkeeping


class BookkeepingRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[Bookkeeping]:
        result = await self._session.scalars(
            select(Bookkeeping).order_by(Bookkeeping.created_at.desc()),
        )
        return list(result.all())

    async def add(self, row: Bookkeeping) -> Bookkeeping:
        self._session.add(row)
        await self._session.flush()
        return row
