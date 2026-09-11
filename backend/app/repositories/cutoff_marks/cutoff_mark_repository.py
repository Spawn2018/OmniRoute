from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cutoff_mark import CutoffMark


class CutoffMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[CutoffMark]:
        packed = await self._session.scalars(
            select(CutoffMark).order_by(
                CutoffMark.mark_code,
                CutoffMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: CutoffMark) -> CutoffMark:
        self._session.add(row)
        await self._session.flush()
        return row
