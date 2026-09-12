from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sid_import_mark import SidImportMark


class SidImportMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[SidImportMark]:
        packed = await self._session.scalars(
            select(SidImportMark).order_by(
                SidImportMark.mark_code,
                SidImportMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: SidImportMark) -> SidImportMark:
        self._session.add(row)
        await self._session.flush()
        return row
