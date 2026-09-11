from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.company_mark import CompanyMark


class CompanyMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[CompanyMark]:
        packed = await self._session.scalars(
            select(CompanyMark).order_by(CompanyMark.mark_code, CompanyMark.id),
        )
        return list(packed.all())

    async def add_mark(self, row: CompanyMark) -> CompanyMark:
        self._session.add(row)
        await self._session.flush()
        return row
