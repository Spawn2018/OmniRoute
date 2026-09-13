from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.po_financing_mark import PoFinancingMark


class PoFinancingMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[PoFinancingMark]:
        packed = await self._session.scalars(
            select(PoFinancingMark).order_by(
                PoFinancingMark.mark_code,
                PoFinancingMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: PoFinancingMark) -> PoFinancingMark:
        self._session.add(row)
        await self._session.flush()
        return row
