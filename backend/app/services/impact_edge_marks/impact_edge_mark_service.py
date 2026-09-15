from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.impact_edge_mark import parse_impact_edge_mark_row
from app.models.impact_edge_mark import ImpactEdgeMark
from app.repositories.impact_edge_marks.impact_edge_mark_repository import (
    ImpactEdgeMarkRepository,
)


class ImpactEdgeMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = ImpactEdgeMarkRepository(session)

    async def list_marks(self) -> list[ImpactEdgeMark]:
        return await self._rows.list_marks()

    async def persist_impact_edge_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        from_kind: object,
        to_kind: object,
        source_ref: object,
    ) -> ImpactEdgeMark:
        code, start, end, origin = parse_impact_edge_mark_row(
            mark_code,
            from_kind,
            to_kind,
            source_ref,
        )
        row = ImpactEdgeMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            from_kind=start,
            to_kind=end,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
