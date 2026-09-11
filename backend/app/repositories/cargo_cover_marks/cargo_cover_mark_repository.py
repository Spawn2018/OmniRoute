from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cargo_cover_mark import CargoCoverMark


class CargoCoverMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[CargoCoverMark]:
        packed = await self._session.scalars(
            select(CargoCoverMark).order_by(
                CargoCoverMark.mark_code,
                CargoCoverMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: CargoCoverMark) -> CargoCoverMark:
        self._session.add(row)
        await self._session.flush()
        return row
