from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.yard_mark import YardMark


class YardMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[YardMark]:
        packed = await self._session.scalars(
            select(YardMark).order_by(
                YardMark.mark_code,
                YardMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: YardMark) -> YardMark:
        self._session.add(row)
        await self._session.flush()
        return row
