from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ais_import_mark import AisImportMark


class AisImportMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[AisImportMark]:
        packed = await self._session.scalars(
            select(AisImportMark).order_by(
                AisImportMark.mark_code,
                AisImportMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: AisImportMark) -> AisImportMark:
        self._session.add(row)
        await self._session.flush()
        return row
