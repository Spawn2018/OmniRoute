from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.blank_sailing_mark import BlankSailingMark


class BlankSailingMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[BlankSailingMark]:
        packed = await self._session.scalars(
            select(BlankSailingMark).order_by(
                BlankSailingMark.mark_code,
                BlankSailingMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: BlankSailingMark) -> BlankSailingMark:
        self._session.add(row)
        await self._session.flush()
        return row
