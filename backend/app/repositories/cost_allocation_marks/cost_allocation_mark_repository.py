from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cost_allocation_mark import CostAllocationMark


class CostAllocationMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[CostAllocationMark]:
        packed = await self._session.scalars(
            select(CostAllocationMark).order_by(
                CostAllocationMark.mark_code,
                CostAllocationMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: CostAllocationMark) -> CostAllocationMark:
        self._session.add(row)
        await self._session.flush()
        return row
