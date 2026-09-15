from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.cost_category_mark import parse_cost_category_mark_row
from app.models.cost_category_mark import CostCategoryMark
from app.repositories.cost_category_marks.cost_category_mark_repository import (
    CostCategoryMarkRepository,
)


class CostCategoryMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = CostCategoryMarkRepository(session)

    async def list_marks(self) -> list[CostCategoryMark]:
        return await self._rows.list_marks()

    async def persist_cost_category_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        category_kind: object,
        source_ref: object,
    ) -> CostCategoryMark:
        code, kind, origin = parse_cost_category_mark_row(
            mark_code,
            category_kind,
            source_ref,
        )
        row = CostCategoryMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            category_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
