from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.line_impact_layer_mark import parse_line_impact_layer_mark_row
from app.models.line_impact_layer_mark import LineImpactLayerMark
from app.repositories.line_impact_layer_marks.line_impact_layer_mark_repository import (
    LineImpactLayerMarkRepository,
)


class LineImpactLayerMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = LineImpactLayerMarkRepository(session)

    async def list_marks(self) -> list[LineImpactLayerMark]:
        return await self._rows.list_marks()

    async def persist_line_impact_layer_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        layer_kind: object,
        source_ref: object,
    ) -> LineImpactLayerMark:
        code, kind, origin = parse_line_impact_layer_mark_row(
            mark_code,
            layer_kind,
            source_ref,
        )
        row = LineImpactLayerMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            layer_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
