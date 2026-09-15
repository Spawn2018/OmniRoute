from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sales_bind_mark import SalesBindMark


class SalesBindMarkRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def list_marks(self) -> list[SalesBindMark]:
        result = await self._db.scalars(
            select(SalesBindMark).order_by(
                SalesBindMark.bind_kind.asc(),
                SalesBindMark.mark_code.asc(),
                SalesBindMark.id.asc(),
            ),
        )
        return list(result.all())

    async def add_mark(self, row: SalesBindMark) -> SalesBindMark:
        self._db.add(row)
        await self._db.flush()
        return row
