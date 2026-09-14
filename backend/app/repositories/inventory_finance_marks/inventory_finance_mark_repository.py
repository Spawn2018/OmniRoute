from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.inventory_finance_mark import InventoryFinanceMark


class InventoryFinanceMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[InventoryFinanceMark]:
        stmt = select(InventoryFinanceMark).order_by(
            InventoryFinanceMark.mark_code,
            InventoryFinanceMark.id,
        )
        return list((await self._session.scalars(stmt)).all())

    async def add_mark(self, row: InventoryFinanceMark) -> InventoryFinanceMark:
        self._session.add(row)
        await self._session.flush()
        return row
