from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.oog_mark import OogMark


class OogMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[OogMark]:
        packed = await self._session.scalars(
            select(OogMark).order_by(OogMark.mark_code, OogMark.id),
        )
        return list(packed.all())

    async def add_mark(self, row: OogMark) -> OogMark:
        self._session.add(row)
        await self._session.flush()
        return row
