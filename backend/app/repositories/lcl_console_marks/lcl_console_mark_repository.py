from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lcl_console_mark import LclConsoleMark


class LclConsoleMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[LclConsoleMark]:
        packed = await self._session.scalars(
            select(LclConsoleMark).order_by(
                LclConsoleMark.mark_code,
                LclConsoleMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: LclConsoleMark) -> LclConsoleMark:
        self._session.add(row)
        await self._session.flush()
        return row
