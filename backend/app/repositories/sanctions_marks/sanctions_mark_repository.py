from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sanctions_mark import SanctionsMark


class SanctionsMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[SanctionsMark]:
        packed = await self._session.scalars(
            select(SanctionsMark).order_by(
                SanctionsMark.mark_code,
                SanctionsMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: SanctionsMark) -> SanctionsMark:
        self._session.add(row)
        await self._session.flush()
        return row
