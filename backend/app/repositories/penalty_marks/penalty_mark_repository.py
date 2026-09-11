from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.penalty_mark import PenaltyMark


class PenaltyMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[PenaltyMark]:
        packed = await self._session.scalars(
            select(PenaltyMark).order_by(PenaltyMark.mark_code, PenaltyMark.id),
        )
        return list(packed.all())

    async def add_mark(self, row: PenaltyMark) -> PenaltyMark:
        self._session.add(row)
        await self._session.flush()
        return row
