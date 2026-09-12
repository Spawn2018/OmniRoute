from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.peppol_mark import PeppolMark


class PeppolMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[PeppolMark]:
        packed = await self._session.scalars(
            select(PeppolMark).order_by(
                PeppolMark.mark_code,
                PeppolMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: PeppolMark) -> PeppolMark:
        self._session.add(row)
        await self._session.flush()
        return row
