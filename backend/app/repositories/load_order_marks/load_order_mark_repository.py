from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.load_order_mark import LoadOrderMark


class LoadOrderMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[LoadOrderMark]:
        packed = await self._session.scalars(
            select(LoadOrderMark).order_by(
                LoadOrderMark.mark_code,
                LoadOrderMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: LoadOrderMark) -> LoadOrderMark:
        self._session.add(row)
        await self._session.flush()
        return row
