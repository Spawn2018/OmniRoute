from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cfo_narrative_mark import CfoNarrativeMark


class CfoNarrativeMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[CfoNarrativeMark]:
        stmt = select(CfoNarrativeMark).order_by(
            CfoNarrativeMark.mark_code,
            CfoNarrativeMark.id,
        )
        return list((await self._session.scalars(stmt)).all())

    async def add_mark(self, row: CfoNarrativeMark) -> CfoNarrativeMark:
        self._session.add(row)
        await self._session.flush()
        return row
