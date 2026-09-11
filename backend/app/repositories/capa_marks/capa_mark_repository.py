from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.capa_mark import CapaMark


class CapaMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[CapaMark]:
        packed = await self._session.scalars(
            select(CapaMark).order_by(CapaMark.mark_code, CapaMark.id),
        )
        return list(packed.all())

    async def add_mark(self, row: CapaMark) -> CapaMark:
        self._session.add(row)
        await self._session.flush()
        return row
