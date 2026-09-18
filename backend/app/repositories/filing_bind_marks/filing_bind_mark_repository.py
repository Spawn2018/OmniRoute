from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.filing_bind_mark import FilingBindMark


class FilingBindMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[FilingBindMark]:
        packed = await self._session.scalars(
            select(FilingBindMark).order_by(FilingBindMark.mark_code, FilingBindMark.id),
        )
        return list(packed.all())

    async def add_mark(self, row: FilingBindMark) -> FilingBindMark:
        self._session.add(row)
        await self._session.flush()
        return row
