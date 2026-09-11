from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cmms_mark import CmmsMark


class CmmsMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[CmmsMark]:
        packed = await self._session.scalars(
            select(CmmsMark).order_by(CmmsMark.mark_code, CmmsMark.id),
        )
        return list(packed.all())

    async def add_mark(self, row: CmmsMark) -> CmmsMark:
        self._session.add(row)
        await self._session.flush()
        return row
