from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.line_impact_mark import parse_line_impact_mark_row
from app.models.line_impact_mark import LineImpactMark
from app.repositories.line_impact_marks.line_impact_mark_repository import (
    LineImpactMarkRepository,
)


class LineImpactMarkService:
    """HITL katalog skutku linii — bez SQL impact i bez EBITDA."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = LineImpactMarkRepository(session)

    async def list_marks(self) -> list[LineImpactMark]:
        return await self._marks.list_marks()

    async def persist_line_impact_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        impact_kind: object,
        source_ref: object,
    ) -> LineImpactMark:
        code, kind, pointer = parse_line_impact_mark_row(
            mark_code,
            impact_kind,
            source_ref,
        )
        row = LineImpactMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            impact_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
