from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cost_category_mark import CostCategoryMark


class CostCategoryMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[CostCategoryMark]:
        packed = await self._session.scalars(
            select(CostCategoryMark).order_by(
                CostCategoryMark.mark_code,
                CostCategoryMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: CostCategoryMark) -> CostCategoryMark:
        self._session.add(row)
        await self._session.flush()
        return row
