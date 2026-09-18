from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.waste_mark import WasteMark


class WasteMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[WasteMark]:
        packed = await self._session.scalars(
            select(WasteMark).order_by(WasteMark.mark_code, WasteMark.id),
        )
        return list(packed.all())

    async def add_mark(self, row: WasteMark) -> WasteMark:
        self._session.add(row)
        await self._session.flush()
        return row
