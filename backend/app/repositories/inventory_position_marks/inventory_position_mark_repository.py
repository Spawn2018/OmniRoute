from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.inventory_position_mark import InventoryPositionMark


class InventoryPositionMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[InventoryPositionMark]:
        packed = await self._session.scalars(
            select(InventoryPositionMark).order_by(
                InventoryPositionMark.mark_code,
                InventoryPositionMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: InventoryPositionMark) -> InventoryPositionMark:
        self._session.add(row)
        await self._session.flush()
        return row
