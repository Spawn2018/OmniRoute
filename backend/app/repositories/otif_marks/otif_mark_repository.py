from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.otif_mark import OtifMark


class OtifMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[OtifMark]:
        packed = await self._session.scalars(
            select(OtifMark).order_by(OtifMark.mark_code, OtifMark.id),
        )
        return list(packed.all())

    async def add_mark(self, row: OtifMark) -> OtifMark:
        self._session.add(row)
        await self._session.flush()
        return row
