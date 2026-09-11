from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.cost_allocation_mark import parse_cost_allocation_mark_row
from app.models.cost_allocation_mark import CostAllocationMark
from app.repositories.cost_allocation_marks.cost_allocation_mark_repository import (
    CostAllocationMarkRepository,
)


class CostAllocationMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = CostAllocationMarkRepository(session)

    async def list_marks(self) -> list[CostAllocationMark]:
        return await self._rows.list_marks()

    async def persist_cost_allocation_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        alloc_kind: object,
        source_ref: object,
    ) -> CostAllocationMark:
        code, kind, origin = parse_cost_allocation_mark_row(
            mark_code,
            alloc_kind,
            source_ref,
        )
        row = CostAllocationMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            alloc_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
