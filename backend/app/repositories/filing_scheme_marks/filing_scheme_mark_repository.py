from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.filing_scheme_mark import FilingSchemeMark


class FilingSchemeMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[FilingSchemeMark]:
        packed = await self._session.scalars(
            select(FilingSchemeMark).order_by(
                FilingSchemeMark.mark_code,
                FilingSchemeMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: FilingSchemeMark) -> FilingSchemeMark:
        self._session.add(row)
        await self._session.flush()
        return row
