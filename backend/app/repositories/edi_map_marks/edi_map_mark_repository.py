from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.edi_map_mark import EdiMapMark


class EdiMapMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[EdiMapMark]:
        packed = await self._session.scalars(
            select(EdiMapMark).order_by(
                EdiMapMark.mark_code,
                EdiMapMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: EdiMapMark) -> EdiMapMark:
        self._session.add(row)
        await self._session.flush()
        return row
