from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.inventory_collateral_mark import InventoryCollateralMark


class InventoryCollateralMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[InventoryCollateralMark]:
        stmt = select(InventoryCollateralMark).order_by(
            InventoryCollateralMark.mark_code,
            InventoryCollateralMark.id,
        )
        return list((await self._session.scalars(stmt)).all())

    async def add_mark(
        self,
        row: InventoryCollateralMark,
    ) -> InventoryCollateralMark:
        self._session.add(row)
        await self._session.flush()
        return row
