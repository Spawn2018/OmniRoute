from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.legal_hold_mark import LegalHoldMark


class LegalHoldMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[LegalHoldMark]:
        packed = await self._session.scalars(
            select(LegalHoldMark).order_by(LegalHoldMark.mark_code, LegalHoldMark.id),
        )
        return list(packed.all())

    async def add_mark(self, row: LegalHoldMark) -> LegalHoldMark:
        self._session.add(row)
        await self._session.flush()
        return row
