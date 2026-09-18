from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.filing_fk_mark import FilingFkMark


class FilingFkMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[FilingFkMark]:
        packed = await self._session.scalars(
            select(FilingFkMark).order_by(
                FilingFkMark.mark_code,
                FilingFkMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: FilingFkMark) -> FilingFkMark:
        self._session.add(row)
        await self._session.flush()
        return row
